# gandi-live-dns
DynDNS Updater for Gandi LiveDNS REST API

## purpose

Add dynamic dns container to any stack.


## quickstart

1. Add the service to your `docker-compose.yml` stack. Hard-coding the parameters is best, we had trouble with quotes when trying to pass it through a `.env` file.

    ```
    version: '3'
    
    services:
      gandi_dns:
        image: anthonymobile/gandi-live-dns
        restart: always
        environment
          - GANDI_API_KEY=afahs4535jsafsf7as8fsfasv7cf4
          - GANDI_DOMAIN=mydomain.com
          - GANDI_SUBDOMAINS=king, queen
    ```

3. Bring up your stack

    ```
    docker-compose up
    ```
## future

The script can handle as many domains and subdomains as you like, but have't figured out a good way to pass them at runtime through `docker-compose`, which won't take an array.