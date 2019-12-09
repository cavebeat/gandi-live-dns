#!/usr/bin/env python3
# encoding: utf-8
'''
Gandi v5 LiveDNS - DynDNS Update via REST API and CURL/requests

@author: cave
@author: dvdme
License GPLv3
https://www.gnu.org/licenses/gpl-3.0.html

Created on 13 Aug 2017
Forked on 08 Dec 2019
http://doc.livedns.gandi.net/
http://doc.livedns.gandi.net/#api-endpoint -> https://dns.gandi.net/api/v5/
'''

import json
import requests
import ipaddress
import config
import argparse
import threading as th
from pprint import pprint


def check_is_ipv6(ip_address, verbose=False):
    return ipaddress.ip_address(ip_address).version == 6


def get_dynip(ifconfig_provider, verbose=False):
    ''' find out own IPv4 at home <-- this is the dynamic IP which changes more or less frequently
    similar to curl ifconfig.me/ip, see example.config.py for details to ifconfig providers 
    '''
    if verbose:
        print(f'Using {ifconfig_provider}')
    r = requests.get(ifconfig_provider)
    print (f'Checking dynamic IP: {r.text.strip()}')
    return r.text.strip()

def get_uuid(verbose=False):
    '''
    find out ZONE UUID from domain
    Info on domain "DOMAIN"
    GET /domains/<DOMAIN>:
    '''
    url = config.api_endpoint + '/domains/' + config.domain
    u = requests.get(url, headers={"X-Api-Key":config.api_secret})
    json_object = u.json()
    if verbose:
        pprint(json_object)
    if u.status_code == 200:
        return json_object['zone_uuid']
    else:
        print(f'Error: HTTP Status Code {u.status_code} when trying to get Zone UUID')
        pprint(u.json())
        exit()

def get_dnsip(uuid, is_ipv6=False, verbose=False):
    ''' find out IP from first Subdomain DNS-Record
    List all records with name "NAME" and type "TYPE" in the zone UUID
    GET /zones/<UUID>/records/<NAME>/<TYPE>:

    The first subdomain from config.subdomain will be used to get
    the actual DNS Record IP
    '''
    if is_ipv6:
        record_type = '/AAAA'
        subdomain = config.subdomains6[0]
    else:
       record_type = '/A'
       subdomain = config.subdomains[0]

    url = config.api_endpoint+ '/zones/' + uuid + '/records/' + subdomain + record_type
    headers = {'X-Api-Key':config.api_secret}
    u = requests.get(url, headers=headers)
    if u.status_code == 200:
        json_object = u.json()
        if verbose:
            pprint(json_object)
        dnsip = json_object['rrset_values'][0].strip()
        print (f'Checking IP from DNS Record {subdomain}: {dnsip}')
        return dnsip
    else:
        print('Error: HTTP Status Code ', u.status_code, 'when trying to get IP from subdomain', subdomain)
        pprint(u.json())
        exit()

def update_records(uuid, dynIP, subdomain, is_ipv6=False, verbose=False):
    ''' update DNS Records for Subdomains
        Change the "NAME"/"TYPE" record from the zone UUID
        PUT /zones/<UUID>/records/<NAME>/<TYPE>:
        curl -X PUT -H "Content-Type: application/json" \
                    -H 'X-Api-Key: XXX' \
                    -d '{"rrset_ttl": 10800,
                         "rrset_values": ["<VALUE>"]}' \
                    https://dns.gandi.net/api/v5/zones/<UUID>/records/<NAME>/<TYPE>
    '''
    if is_ipv6:
        record_type = '/AAAA'
    else:
       record_type = '/A'
    url = config.api_endpoint+ '/zones/' + uuid + '/records/' + subdomain + record_type
    payload = {'rrset_ttl': config.ttl, "rrset_values": [dynIP]}
    headers = {'Content-Type': 'application/json', 'X-Api-Key':config.api_secret}
    u = requests.put(url, data=json.dumps(payload), headers=headers)
    json_object = u.json()
    if u.status_code == 201:
        print (f'Status Code: {u.status_code}, {json_object["message"]}, IP updated for {subdomain}')
        return True
    else:
        print (f'Error: HTTP Status Code {u.status_code} when trying to update IP from subdomain {subdomain}')
        print (json_object['message'])
        exit()



def main(force_update, verbosity, repeat):

    if verbosity:
        print('verbosity turned on')
        verbose = True
    else:
        verbose =False

    if repeat and verbose:
        print(f'repeat turned on, will repeat every {repeat} seconds')

    #get zone ID from Account
    uuid = get_uuid()

    #compare dynIP and DNS IP
    dynIP = get_dynip(config.ifconfig, verbose)

    if check_is_ipv6(dynIP, verbose):
        subdomains = config.subdomains6
        is_ipv6 = True
        print('Detected ipv6')
    else:
        print('Detected ipv4')
        is_ipv6 = False
        subdomains = config.subdomains

    dnsIP = get_dnsip(uuid, is_ipv6, verbose)

    if force_update:
        print ('Going to update/create the DNS Records for the subdomains')
        for sub in subdomains:
            update_records(uuid, dynIP, sub, is_ipv6, verbose)
    else:
        if verbose:
            print(f'dynIP: {dynIP}')
            print(f'dnsIP: {dnsIP}')
        if dynIP == dnsIP:
            print ('IP Address Match - no further action')
        else:
            print (f'IP Address Mismatch - going to update the DNS Records for the subdomains with new IP {dynIP}')
            for sub in subdomains:
                update_records(uuid, dynIP, sub, is_ipv6, verbose)
    if repeat:
        if verbosity:
            print(f'Repeating in {repeat} seconds')
        th.Timer(repeat, main, [force_update, verbosity, repeat]).start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
    parser.add_argument('-f', '--force', help='force an update/create', action='store_true')
    parser.add_argument('-r', '--repeat', type=int, help='keep running and repeat every N seconds')
    args = parser.parse_args()
    main(args.force, args.verbose, args.repeat)
