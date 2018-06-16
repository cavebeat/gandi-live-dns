#!/usr/bin/env python
# encoding: utf-8

import ConfigParser
from ConfigParser import NoOptionError
import os

snap = os.environ['SNAP_NAME']
config_file = os.path.join(os.environ['SNAP_DATA'], 'config')

def error_msg(key):
    return ("No `{key}` value set, you need to configure this snap using " \
        "`snap set {snap} {key}=<value>`".format(key=key, snap=snap))

if not os.path.exists(config_file):
    raise Exception("No configuration file found at {}".format(config_file))

try:
    config = ConfigParser.ConfigParser()
    config.readfp(open(config_file))
except:
    raise Exception("Impossible to open config file {}".format(config_file))

def get_setting(key):
    try:
        s = config.get('settings', key)
        if not len(s):
            raise NoOptionError('settings', key)
    except NoOptionError as e:
        raise e
    return s

try:
    api_secret = get_setting('apisecret')
except NoOptionError as e:
    print(error_msg("apisecret"))
    print('''
    Get your API key
    Start by retrieving your API Key from the "Security" section in new Account admin panel to be able to make authenticated requests to the API.
    https://account.gandi.net/
    ''')
    raise e

try:
    api_endpoint = get_setting('apiendpoint')
except NoOptionError as e:
    api_endpoint = 'https://dns.api.gandi.net/api/v5'

try:
    domain = config.get("settings", "domain")
except NoOptionError as e:
    print(error_msg("domain"))
    raise e

try:
    subdomains = get_setting('subdomains').split(',')
except NoOptionError as e:
    subdomains = ''

try:
    ttl = get_setting('ttl')
except NoOptionError as e:
    ttl = '300'

try:
    ifconfig = get_setting('ifconfig')
except NoOptionError as e:
    ifconfig = 'http://ipv4.myexternalip.com/raw'
