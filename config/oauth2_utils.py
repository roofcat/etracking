# encoding:utf-8
#!/usr/bin/env python

from oauth2client.appengine import OAuth2Decorator
from apiclient.discovery import build
from google.appengine.api import memcache


import httplib2


http = httplib2.Http(memcache)
user_info_service = build('oauth2', 'v2', http=http)
decorator = OAuth2Decorator(
    client_id='283143445923-dpq576riobmgku51ohqnga3hlb76o038.apps.googleusercontent.com',
    client_secret='BUtkierbnmipwyc7GjmjkyIs',
    scope='https://www.googleapis.com/auth/userinfo.profile ' +
    'https://www.googleapis.com/auth/userinfo.email '
)