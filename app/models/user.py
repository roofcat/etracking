# -*- coding: utf-8 -*-
#!/usr/bin/env python


from google.appengine.ext import ndb


class UserModel(ndb.Model):
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    enterprise = ndb.StringProperty(required=True)
