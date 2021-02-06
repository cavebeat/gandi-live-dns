#!/usr/bin/env python
# encoding: utf-8
'''
Gandi v5 LiveDNS - DynDNS Update via REST API and CURL/requests

@author: cave
License GPLv3
https://www.gnu.org/licenses/gpl-3.0.html

Created on 13 Aug 2017
http://doc.livedns.gandi.net/ 
http://doc.livedns.gandi.net/#api-endpoint -> https://dns.gandi.net/api/v5/
'''

import requests, json
import config
import argparse

api_endpoint = 'https://api.gandi.net/v5/livedns/domains/'

headers = {"Content-Type": "application/json", "Authorization": "Apikey " + config.api_secret}

def get_dynip(ifconfig_provider):
    ''' find out own IPv4 at home <-- this is the dynamic IP which changes more or less frequently
    similar to curl ifconfig.me/ip, see example.config.py for details to ifconfig providers 
    ''' 
    r = requests.get(ifconfig_provider)
    print 'Checking dynamic IP:', r._content.strip('\n')
    return r.content.strip('\n')

def get_dnsip(subdomain):
    '''Finds A record for subdomain'''
    url = api_endpoint + config.domain + "/records/" + subdomain

    u = requests.get(url + "/A", headers=headers)
    json_object = json.loads(u._content)
    if u.status_code == 200:
        return json_object['rrset_values'][0].encode('ascii','ignore').strip('\n')
    else:
        print '[%s] Error: HTTP Status Code %s when trying to get IP' % (subdomain, u.status_code)
        print json_object['message']
        exit()

def update_records(dynIP, subdomain):
    '''Update DNS Records for a subdomain'''
    payload = {"items": [{"rrset_ttl": config.ttl, "rrset_values": [dynIP], "rrset_type": "A"}]}
    url = api_endpoint + config.domain + "/records/" + subdomain
    u = requests.put(url, data=json.dumps(payload), headers=headers)
    json_object = json.loads(u._content)
    if u.status_code == 201:
        print '[%s] IP updated, status code: %s: %s' % (subdomain, u.status_code, json_object['message'])
        return True
    else:
        print '[%s] Error when updating IP, status code: %s: %s' % (subdomain, u.status_code, json_object['message'])
        exit()

def main(force_update, verbosity):

    if verbosity:
        print "verbosity turned on - not implemented by now"
        
    #compare dynIP and DNS IP 
    dynIP = get_dynip(config.ifconfig)
    for subdomain in config.subdomains:
        dnsIP = get_dnsip(subdomain)
        if dynIP == dnsIP:
            print "[%s] IP Address Match - no further action" % subdomain
        else:
            print "[%s] IP Address Mismatch - updating %s to %s" % (subdomain, dnsIP, dynIP)
            update_records(dynIP, subdomain)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help="increase output verbosity", action="store_true")
    parser.add_argument('-f', '--force', help="force an update/create", action="store_true")
    args = parser.parse_args()
        
        
    main(args.force, args.verbose)
