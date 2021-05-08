# gandi-live-dns
DynDNS Updater for Gandi LiveDNS REST API

## purpose

Add dynamic dns container to any stack.


## quickstart

1. create or append the following to your `.env` file

    ```
    GANDI_API_KEY='afahs4535jsafsf7as8fsfasv7cf4'
    GANDI_DOMAIN='mydomain.com'
    GANDI_SUBDOMAINS='king, queen'
    ```
 
2. Add the service to your `docker-compose.yml` stack.

    ```
    version: '3'
    
    services:
      gandi_dns:
        image: anthonymobile/gandi-live-dns
        restart: always
        environment
          - GANDI_API_KEY=$GANDI_API_KEY
          - GANDI_DOMAIN=$GANDI_DOMAIN
          - GANDI_SUBDOMAINS=$GANDI_SUBDOMAINS
    ```

3. Bring up your stack

    ```
    docker-compose up
    ```
## future

The script can handle as many domains and subdomains as you like, but have't figured out a good way to pass them at runtime through `docker-compose`, which won't take an array.