# -*- coding: utf-8 -*-
#!/usr/bin/env python


from google.appengine.ext import ndb


class UserModel(ndb.Model):
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    enterprise = ndb.StringProperty(required=True)
    is_admin = ndb.BooleanProperty(default=False)
    is_custom_user = ndb.BooleanProperty(default=True)

    def get_user(self, email):
    	return UserModel.query(UserModel.email == email).get()