#!/usr/bin/env python
# encoding: utf-8
'''
Gandi v5 LiveDNS - DynDNS Update via REST API and CURL/requests

@author: cave
License GPLv3
https://www.gnu.org/licenses/gpl-3.0.html

Created on 13 Aug 2017
http://doc.livedns.gandi.net/ 
http://doc.livedns.gandi.net/#api-endpoint -> https://dns.beta.gandi.net/api/v5/
'''

import json
import logging
import logging.config
import requests
import config
import argparse

logging.config.dictConfig(config.log_config)
log = logging.getLogger('gandi-live-dns')

def get_dynip(ifconfig_provider):
    ''' find out own IPv4 at home <-- this is the dynamic IP which changes more or less frequently
    similar to curl ifconfig.me/ip, see example.config.py for details to ifconfig providers 
    ''' 
    log.debug('Using ifconfig_provider {}'.format(ifconfig_provider))
    r = requests.get(ifconfig_provider)
    log.info('Checking dynamic IP: {}'.format(r.text.strip('\n')))
    return r.text.strip('\n')

def get_uuid():
    ''' 
    find out ZONE UUID from domain
    Info on domain "DOMAIN"
    GET /domains/<DOMAIN>:
        
    '''
    url = config.api_endpoint + '/domains/' + config.domain
    log.debug('Using url {}'.format(url))
    u = requests.get(url, headers={"X-Api-Key":config.api_secret})
    json_object = u.json()
    if u.status_code == 200:
        return json_object['zone_uuid']
    else:
        log.error('Error: HTTP Status Code {} when trying to get Zone UUID'.format(u.status_code))
        log.error('{}'.format(json_object['message']))
        exit()

def get_dnsip(uuid):
    ''' find out IP from first Subdomain DNS-Record
    List all records with name "NAME" and type "TYPE" in the zone UUID
    GET /zones/<UUID>/records/<NAME>/<TYPE>:
    
    The first subdomain from config.subdomain will be used to get   
    the actual DNS Record IP
    '''

    url = config.api_endpoint+ '/zones/' + uuid + '/records/' + config.subdomains[0] + '/A'
    log.debug('Using url {}'.format(url))    
    headers = {"X-Api-Key":config.api_secret}
    log.debug('Using headers {}'.format(headers))    
    u = requests.get(url, headers=headers)
    if u.status_code == 200:
        json_object = u.json()
        log.info('Checking IP from DNS Record {} : {}'.format(config.subdomains[0], json_object['rrset_values'][0].strip('\n')))
        return json_object['rrset_values'][0].strip('\n')
    else:
        log.error('Error: HTTP Status Code {} when trying to get IP from subdomain {}'.format(u.status_code, config.subdomains[0]))
        log.error('{}'.format(json_object['message']))
        exit()

def update_records(uuid, dynIP, subdomain):
    ''' update DNS Records for Subdomains 
        Change the "NAME"/"TYPE" record from the zone UUID
        PUT /zones/<UUID>/records/<NAME>/<TYPE>:
        curl -X PUT -H "Content-Type: application/json" \
                    -H 'X-Api-Key: XXX' \
                    -d '{"rrset_ttl": 10800,
                         "rrset_values": ["<VALUE>"]}' \
                    https://dns.beta.gandi.net/api/v5/zones/<UUID>/records/<NAME>/<TYPE>
    '''
    url = config.api_endpoint+ '/zones/' + uuid + '/records/' + subdomain + '/A'
    log.debug('Using url {}'.format(url))        
    payload = {"rrset_ttl": config.ttl, "rrset_values": [dynIP]}
    log.debug('Using payload {}'.format(payload))        
    headers = {"Content-Type": "application/json", "X-Api-Key":config.api_secret}
    log.debug('Using headers {}'.format(headers))        
    u = requests.put(url, data=json.dumps(payload), headers=headers)
    json_object = u.json()

    if u.status_code == 201:
        log.info('Status Code: {}, {}, IP updated for {}'.format(u.status_code, json_object['message'], subdomain))
        return True
    else:
        log.error('Error: HTTP Status Code {} when trying to update IP from subdomain {}'.format(u.status_code, subdomain))   
        log.error('{}'.format(json_object['message']))
        exit()



def main(force_update, verbosity):

    if verbosity:
        log.setLevel(logging.DEBUG)
        log.debug('Verbosity On')

    #get zone ID from Account
    uuid = get_uuid()
    log.debug('uuid: {}'.format(uuid))
   
    #compare dynIP and DNS IP 
    dynIP = get_dynip(config.ifconfig)
    dnsIP = get_dnsip(uuid)
    log.debug('dynIP: {}, dnsIP: {}'.format(dynIP, dnsIP))
    
    if force_update:
        log.info("Going to update/create the DNS Records for the subdomains")
        for sub in config.subdomains:
            log.debug('Forcing update on {}'.format(sub))
            update_records(uuid, dynIP, sub)
    else:
        if dynIP == dnsIP:
            log.info("IP Address Match - no further action")
        else:
            log.info("IP Address Mismatch - going to update the DNS Records for the subdomains with new IP", dynIP)
            for sub in config.subdomains:
                log.debug('Updating on {}'.format(sub))                
                update_records(uuid, dynIP, sub)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help="increase output verbosity", action="store_true")
    parser.add_argument('-f', '--force', help="force an update/create", action="store_true")
    args = parser.parse_args()
    main(args.force, args.verbose)
    