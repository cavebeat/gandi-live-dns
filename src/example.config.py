'''
Created on 13 Aug 2017
@author: cave
Copy this file to config.py and update the settings
'''
#!/usr/bin/env python
# encoding: utf-8

'''
Get your API key
Start by retrieving your API Key from the "Security" section in new Account admin panel to be able to make authenticated requests to the API.
https://account.gandi.net/
'''
api_secret = '---my_secret_API_KEY----'

'''
Gandiv5 LiveDNS API Location
http://doc.livedns.gandi.net/#api-endpoint
https://dns.api.gandi.net/api/v5/
'''
api_endpoint = 'https://dns.api.gandi.net/api/v5'

#your domain with the subdomains in the zone file/UUID
domain = 'mydomain.tld'

#enter all subdomains to be updated, subdomains must already exist to be updated
subdomains = ["subdomain1", "subdomain2", "subdomain3"]

#300 seconds = 5 minutes
ttl = '300'

'''
IP address lookup service
run your own external IP provider:
+ https://github.com/mpolden/ipd
+ <?php $ip = $_SERVER['REMOTE_ADDR']; ?>
  <?php print $ip; ?>
e.g.
+ https://[v4|v6].ifconfig.co/ip
+ http://ifconfig.me/ip
+ http://whatismyip.akamai.com/
+ http://ipinfo.io/ip
+ many more ...
'''
#Leave blank to not update that protocol (v4 or v6)
ifconfigv4 = 'choose_from_above_or_run_your_own'
ifconfigv6 = 'choose_from_above_or_run_your_own'
