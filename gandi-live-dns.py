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

Rewrite for multi-domain
Anthony Townsend
2021 May

'''

import json, requests, argparse
from config import config


def get_myip(ifconfig_provider):
    r = requests.get(ifconfig_provider)
    print('\nChecking my IP: ', r._content.decode("utf-8").strip('\n'))
    return r.content.decode("utf-8").strip('\n')

def get_uuid(domain):
    ''' 
    find out ZONE UUID from domain
    Info on domain "DOMAIN"
    GET /domains/<DOMAIN>:
        
    '''
    url = config.api_endpoint + '/domains/' + domain
    u = requests.get(url, headers={"X-Api-Key": config.api_secret})
    json_object = json.loads(u._content)
    if u.status_code == 200:
        return json_object['zone_uuid']
    else:
        print(('Error: HTTP Status Code ', u.status_code, 'when trying to get Zone UUID'))
        print((json_object['message']))
        exit()

def get_dnsip(uuid,subdomain,fully_qualified):
    ''' find out IP from first Subdomain DNS-Record
    List all records with name "NAME" and type "TYPE" in the zone UUID
    GET /zones/<UUID>/records/<NAME>/<TYPE>:
    
    The first subdomain from config.subdomain will be used to get   
    the actual DNS Record IP
    '''

    url = config.api_endpoint + '/zones/' + uuid + '/records/' + subdomain + '/A'
    headers = {"X-Api-Key": config.api_secret}
    u = requests.get(url, headers=headers)
    if u.status_code == 200:
        json_object = json.loads(u._content)
        print('\nChecking IP from DNS Record', config.subdomains[0], ':', json_object['rrset_values'][0])
        return True, json_object['rrset_values'][0]
    else:
        # print('ERROR ({}) Error: HTTP Status Code {} when trying to get IP — subdomain or domain probably doesnt exist.'.format(fully_qualified, u.status_code))
        return False, None

def update_records(uuid, dynIP, subdomain):
    ''' update DNS Records for Subdomains 
        Change the "NAME"/"TYPE" record from the zone UUID
        PUT /zones/<UUID>/records/<NAME>/<TYPE>:
        curl -X PUT -H "Content-Type: application/json" \
                    -H 'X-Api-Key: XXX' \
                    -d '{"rrset_ttl": 10800,
                         "rrset_values": ["<VALUE>"]}' \
                    https://dns.gandi.net/api/v5/zones/<UUID>/records/<NAME>/<TYPE>
    '''
    url = config.api_endpoint + '/zones/' + uuid + '/records/' + subdomain + '/A'
    payload = {"rrset_ttl": config.ttl, "rrset_values": [dynIP]}
    headers = {"Content-Type": "application/json", "X-Api-Key": config.api_secret}
    u = requests.put(url, data=json.dumps(payload), headers=headers)
    json_object = json.loads(u._content)

    if u.status_code == 201:
        # print('Status Code:', u.status_code, ',', json_object['message'], ', IP updated for', subdomain)
        return True
    else:
        print('Error: HTTP Status Code ', u.status_code, 'when trying to update IP from subdomain', subdomain)
        print(json_object['message'])
        return




if __name__ == "__main__":
    print("Gandi DNS Updater v1.1 May 2021, by Anthony Townsend")

    # parser = argparse.ArgumentParser()
    # # parser.add_argument('-v', '--verbose', help="increase output verbosity", name="verbosity", action="store_true")
    # parser.add_argument('-f', '--force', help="force an update/create", action="store_true")
    # args = parser.parse_args()
        
    # if verbosity:
    #     print("Running in verbose mode.")

    # get current IP

    myIP = get_myip(config.ifconfig)

    for domain,subdomains in config.domain_dict.items():

        uuid = get_uuid(domain)
        print ('\n***Using UUID {} for domain {}'.format(uuid,domain))

        for subdomain in subdomains:

            fully_qualified = '.'.join((domain,subdomain))
            exists, dnsIP=get_dnsip(uuid,subdomain,fully_qualified)

            if exists == True:

                # no update needed
                if myIP == dnsIP:
                    print ('NO UPDATE ({}) DNS IP {} matches Host IP {}'.format(fully_qualified,dnsIP,myIP))
                #  update needed
                elif myIP != dnsIP:
                    try:
                        update_records(uuid, myIP, subdomain)
                        print('UPDATED ({}) DNS IP {} changed to match Host IP {}'.format(fully_qualified,dnsIP,myIP))
                    except:
                        print('ERROR ({}) Update failed'.format(fully_qualified))
                        pass

            elif exists == False:
                print('ERROR ({}) Update failed, no DNS record for subdomain or domain.'.format(fully_qualified))
