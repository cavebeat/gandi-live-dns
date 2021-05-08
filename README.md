# gandi-live-dns
DynDNS Updater for Gandi LiveDNS REST API

## purpose

Add dynamic dns container to any stack.


## quickstart

1. create or append the following to your a `.env` file

    ```
    API_KEY='afahs4535jsafsf7as8fsfasv7cf4'
    
    DOMAIN_DICT = "{'urbantech.live':['test1'],'urbantechhub.io':['test1','test2'],'cornellurban.tech':['test1','test2','test3']}"
    ```
    
2. Add the service to your `docker-compose.yml` stack.

    ```
    version: '3'
    
    services:
      gandi_dns:
        image: anthonymobile/gandi-live-dns
        restart: always
    
    ```

3. Bring up your stack

    ```
    docker-compose up
    ```
