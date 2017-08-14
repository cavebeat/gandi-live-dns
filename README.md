gandi_live_dns
----

This is a simple dynamic DNS updater for the
[Gandi](https://www.gandi.net) registrar. It uses their REST API to update
the zone file for a subdomain of a domain name to point at the external IPv4
address of the computer it has been run from.

It has been developed and tested on Debian 8 Jessie GNU/Linux using Python 2.7.

This DynDNS updater is inspired by https://github.com/jasontbradshaw/gandi-dyndns which worked very well 
with the classic DNS from Gandi v4Website and their XML-RPC API. 
With the new v5 Website, Gandi has also launched a 
new REST API which makes it easier to communicate via bash/curl or python/requests.  

### Walkthrough

You want your homeserver to be always available at `dynamic.mydomain.tld`.

#### API Key
First, you must apply for an API key with Gandi. Visit
https://account.gandi.net/en/ and apply for (at least) the production API
key by following their directions.

#### A Record Setup
Create the DNS A Records in the GANDI Webinterface which you want to update if your IP changes. 

#### Script Configuration
Then you'd need to configure the script.

Copy `example.config.py` to `config.py`, and put it in the same directory
   as the script.

   
yada yada ... 
more to come