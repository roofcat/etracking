# encoding: utf-8
#!/usr/bin/env python

from oauth2client.appengine import OAuth2Decorator
from apiclient.discovery import build
from google.appengine.api import memcache


import httplib2
import urllib2


http = httplib2.Http(memcache)

user_info_service = build('oauth2', 'v2', http=http)

decorator = OAuth2Decorator(
    client_id='966736474928-bsqgnmqf8u6bs4chucuacrrch2amgmen.apps.googleusercontent.com',
    client_secret='GylHPpGJSYDCdKumG8wQj-ul',
    approval_prompt='force',
    scope='https://www.googleapis.com/auth/userinfo.profile ' +
    'https://www.googleapis.com/auth/userinfo.email ',
)

def revoke_access_token(token):
    """
    Permite al usuario eliminar permiso de acceso a la aplicación
    """
    return urllib2.urlopen('https://accounts.google.com/o/oauth2/revoke?token=%s' % token)
