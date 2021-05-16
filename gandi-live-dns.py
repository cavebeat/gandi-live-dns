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

import json, requests, os

#300 seconds = 5 minutes
ttl = '300'

# Gandiv5 LiveDNS API Location
# http://doc.livedns.gandi.net/#api-endpoint
# https://dns.api.gandi.net/api/v5/
api_endpoint = 'https://dns.api.gandi.net/api/v5'


# IP address lookup service
# run your own external IP provider:
# + https://github.com/mpolden/ipd
# + <?php $ip = $_SERVER['REMOTE_ADDR']; ?>
#   <?php print $ip; ?>
# e.g.
# + https://ifconfig.co/ip
# + http://ifconfig.me/ip
# + http://whatismyip.akamai.com/
# + http://ipinfo.io/ip
# + many more ...

# ifconfig = 'https://ifconfig.co/ip'
ip_lookup_url = 'http://ipinfo.io/ip'


def get_env():
    api_key = os.environ['GANDI_API_KEY']
    #todo figure out a way of passing more than one domain in here from .env
    domain_dict = { os.environ['GANDI_DOMAIN']: os.environ['GANDI_SUBDOMAINS'].split(',') }
    return api_key, domain_dict

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
    url = api_endpoint + '/domains/' + domain
    u = requests.get(url, headers={"X-Api-Key": api_key})
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

    url = api_endpoint + '/zones/' + uuid + '/records/' + subdomain + '/A'
    headers = {"X-Api-Key": api_key}
    u = requests.get(url, headers=headers)
    if u.status_code == 200:
        json_object = json.loads(u._content)
        print('\nChecking IP from DNS Record', subdomain, ':', json_object['rrset_values'][0])
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
    url = api_endpoint + '/zones/' + uuid + '/records/' + subdomain + '/A'
    payload = {"rrset_ttl": ttl, "rrset_values": [dynIP]}
    headers = {"Content-Type": "application/json", "X-Api-Key": api_key}
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

    # future production switch (or a debugging one) limit output to a single print line when a DNS IP is updated


    print("Gandi DNS Updater v1.1 May 2021, by Anthony Townsend")

    # read the domain_dict and APIkey from .env
    api_key, domain_dict = get_env()
    print('Using api_key from $GANDI_API_KEY: {}'.format(api_key))

    # get current IP
    myIP = get_myip(ip_lookup_url)

    for domain,subdomains in domain_dict.items():

        uuid = get_uuid(domain)
        print ('\n***Using UUID {} for domain {}'.format(uuid,domain))

        for subdomain in subdomains:

            fully_qualified = '.'.join((subdomain,domain,))
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
