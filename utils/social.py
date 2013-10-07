#!/usr/bin/env python
#-*- coding:utf-8 -*-

import urllib2
import urllib
import json

from bae.core import const

AK = const.ACCESS_KEY
SK = const.SECRET_KEY

OAUTH_URL = 'https://openapi.baidu.com/social/oauth/2.0/token'
API_URL   = 'https://openapi.baidu.com/social/api/2.0'

def http_get(url, data) :
  url = url + '?' + urllib.urlencode(data)
  return json.load(urllib2.urlopen(url))

def get_access_token(code) :
  data = {}
  data['grant_type'] = 'authorization_code'
  data['client_id'] = AK
  data['client_secret'] = SK
  data['redirect_uri'] = 'http://hamilton.duapp.com/oauth/callback'
  data['code'] = code
  
  return http_get(OAUTH_URL, data)

def get_user_info(access_token) :
  data = {}
  data['access_token'] = access_token

  return http_get(API_URL + '/user/info', data)

