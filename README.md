gandi-live-dns
----

This is a simple dynamic DNS updater for the
[Gandi](https://www.gandi.net) registrar. It uses their [LiveDNS REST API](http://doc.livedns.gandi.net/) to update the zone file for a subdomain of a domain to point at the external IPv4 address of the computer it has been run from.

It has been developed on Debian 8 Jessie and tested on Debian 9 Stretch GNU/Linux using Python 2.7.

With the new v5 Website, Gandi has also launched a new REST API which makes it easier to communicate via bash/curl or python/requests.  

### Goal

You want your homeserver to be always available at `dynamic_subdomain.mydomain.tld`.

### Debian Package Requirements

`apt-get update && apt-get upgrade && apt-get install unzip python-requests python-args python-simplejson`

#### API Key
First, you must apply for an API key with Gandi. Visit 
https://account.gandi.net/en/ and apply for (at least) the production API 
key by following their directions.

#### A DNS Record 
Create the DNS A Records in the GANDI Webinterface which you want to update if your IP changes. 

#### Git Clone or Download the Script
Download the Script from here as [zip](https://github.com/cavebeat/gandi-live-dns/archive/master.zip)/[tar.gz](https://github.com/cavebeat/gandi-live-dns/archive/master.tar.gz) and extract it.  

or clone from git

`git clone https://github.com/cavebeat/gandi-live-dns.git` 

#### Script Configuration
Then you'd need to configure the script in the src directory.
Copy `example.config.py` to `config.py`, and put it in the same directory as the script.

Edit the config file to fit your needs. 

##### api_secret
Start by retrieving your API Key from the "Security" section in new [Gandi Account admin panel](https://account.gandi.net/) to be able to make authenticated requests to the API.
api_secret = '---my_secret_API_KEY----'

##### domain
Your domain for the subdomains to be updated 


##### subdomains
All subdomains which should be updated. They get created if they do not yet exist.

``` 
subdomains = ["subdomain1", "subdomain2", "subdomain3"]
```
The first subdomain is used to find out the actual IP in the Zone Records. 

#### Run the script
And run the script:

```
root@dyndns:~/gandi-live-dns-master/src# ./gandi-live-dns.py   
Checking dynamic IP: 127.0.0.1
[subdomain1] IP Address Match - no further action
```

If your IP has changed, it will be detected and the update will be triggered. 


```
root@dyndns:~/gandi-live-dns-master/src# ./gandi-live-dns.py
Checking dynamic IP: 127.0.0.2
[subdomain1] IP Address Mismatch - updating 127.0.0.1 to 127.0.0.2
[subdomain1] IP updated, status code: 201: DNS Record Created
```

#### Command Line Arguments

```
root@dyndns:~/gandi-live-dns-master/src# ./gandi-live-dns.py -h
usage: gandi-live-dns.py [-h] [-f]

optional arguments:
  -h, --help     show this help message and exit
  -f, --force    force an update/create

```

The force option runs the script, even when no IP change has been detected. 
It will update all subdomains and even create them if they are missing in the 
Zone File/Zone UUID. This can be used if additional/new subdomains get appended to the conig file.  

### IP address lookup service 
There exist several providers for this case, but better is to run your own somewhere. 

#### Poor Mans PHP Solution
On a LAMP Stack, place the file [index.php](https://github.com/cavebeat/gandi-live-dns/blob/master/src/example-index.php) in a directory /ip in your webroot. 

```
root@laptop:~# curl https://blog.cavebeat.org/ip/
127.0.0.1
```
This should fit your personal needs and you still selfhost the whole thing. 

####  IP address lookup service https://ifconfig.co
https://github.com/mpolden/ipd A simple service for looking up your IP address. This is the code that powers [https://ifconfig.co](https://ifconfig.co)

#### use external services
choose one as described in the config file. 

### Cron the script

Run the script every five minutes. 
```
*/5 * * * * /root/gandi-live-dns-master/src/gandi-live-dns.py >/dev/null 2>&1 
```
### Limitations
The XML-RPC API has a limit of 30 requests per 2 seconds, so i guess it's safe to update 25 subdomains at once with the REST API. 


### Upcoming Features
* command line Argument for verbose mode

### Inspiration   

This DynDNS updater is inspired by https://github.com/jasontbradshaw/gandi-dyndns which worked very well 
with the classic DNS from Gandiv4 Website and their XML-RPC API.

Gandi has created a new API, i accidently switched to the new DNS Record System, so someone had to start a new updater.  
