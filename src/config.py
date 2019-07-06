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
api_secret = ''

'''
Gandiv5 LiveDNS API Location
http://doc.livedns.gandi.net/#api-endpoint
https://dns.api.gandi.net/api/v5/
'''
api_endpoint = 'https://dns.api.gandi.net/api/v5'

#your domain with the subdomains in the zone file/UUID 
domain = ''

#enter all subdomains to be updated, subdomains must already exist to be updated
subdomains = []

#300 seconds = 5 minutes
ttl = '300'

''' 
IP address lookup service 
run your own external IP provider:
+ https://github.com/mpolden/ipd
+ <?php $ip = $_SERVER['REMOTE_ADDR']; ?>
  <?php print $ip; ?>
e.g. 
+ https://ifconfig.co/ip
+ http://ifconfig.me/ip
+ http://whatismyip.akamai.com/
+ http://ipinfo.io/ip
+ many more ...
'''
ifconfig = 'http://whatismyip.akamai.com/'
