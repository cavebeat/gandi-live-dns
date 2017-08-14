'''
Gandi v5 LiveDNS - DynDNS Update via REST API and CURL/requests

@author: cave
Licsense GPLv3
https://www.gnu.org/licenses/gpl-3.0.html

Created on 13 Aug 2017
http://doc.livedns.gandi.net/ 
http://doc.livedns.gandi.net/#api-endpoint -> https://dns.beta.gandi.net/api/v5/
'''

import requests, json
import config


def get_dynip(ifconfig_provider):
    ''' find out own IPv4 at home <-- this is the dynamic IP which changes more or less frequently
    similar to curl ifconfig.me/ip, see example.config.py for details to ifconfig providers 
    ''' 
    r = requests.get(ifconfig_provider)
    print 'Checking dynamic IP: ' , r._content.strip('\n')
    return r.content.strip('\n')

def get_uuid():
    ''' 
    find out ZONE UUID from domain
    Info on domain "DOMAIN"
    GET /domains/<DOMAIN>:
        
    '''
    url = config.api + '/domains/' + config.domain
    u = requests.get(url, headers={"X-Api-Key":config.api_secret})
    json_object = json.loads(u._content)
    return json_object['zone_uuid']

def get_dnsip(uuid):
    ''' find out IP from first Subdomain DNS-Record
    List all records with name "NAME" and type "TYPE" in the zone UUID
    GET /zones/<UUID>/records/<NAME>/<TYPE>:
    '''

    url = config.api + '/zones/' + uuid + '/records/' + config.subdomains[0] + '/A'
    headers = {"X-Api-Key":config.api_secret}
    u = requests.get(url, headers=headers)
    json_object = json.loads(u._content)
    print 'Checking IP from DNS Record' , config.subdomains[0], ' : ', json_object['rrset_values'][0].encode('ascii','ignore').strip('\n')
    return json_object['rrset_values'][0].encode('ascii','ignore').strip('\n')

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
    url = config.api + '/zones/' + uuid + '/records/' + subdomain + '/A'
    payload = {"rrset_ttl": config.ttl, "rrset_values": [dynIP]}
    headers = {"Content-Type": "application/json", "X-Api-Key":config.api_secret}
    record_update = requests.put(url, data=json.dumps(payload), headers=headers)
    json_object = json.loads(record_update._content)
    print 'Status Code: ', record_update.status_code, ', ', json_object['message'], ', IP updated for', subdomain
    return True


def main():
    
    #get zone ID from Account
    uuid = get_uuid()
   
    #compare dynIP and DNS IP 
    dynIP = get_dynip(config.ifconfig)
    dnsIP = get_dnsip(uuid)
    
    if dynIP == dnsIP:
        print "IP Address match - no further action"
    else:
        print "IP Address mismatch - going to update the DNS Records for the subdomains"
        for sub in config.subdomains:
            update_records(uuid, dynIP, sub)

if __name__ == "__main__":
    main()





    