# -*- coding: utf-8 -*-
#!/usr/bin/env python


import webapp2
import json
import base64


from config.oauth2_utils import decorator
from config.oauth2_utils import user_info_service
from config.jinja_environment import JINJA_ENVIRONMENT


from app.models.user import UserModel


class UserAdminHandler(webapp2.RequestHandler):

    @decorator.oauth_required
    def get(self):
        http = decorator.http()
        data = user_info_service.userinfo().get().execute(http=http)
        template = JINJA_ENVIRONMENT.get_template('user/index.html')
        context = {
            'data': data,
        }
        self.response.write(template.render(context))


class ListUserAdminHandler(webapp2.RequestHandler):

    @decorator.oauth_required
    def get(self):
        http = decorator.http()
        data = user_info_service.userinfo().get().execute(http=http)
        users = UserModel.query().fetch()
        self.response.write(json.dumps(users))


class NewUserAdminHandler(webapp2.RequestHandler):

    @decorator.oauth_required
    def get(self):
        http = decorator.http()
        data = user_info_service.userinfo().get().execute(http=http)
        template = JINJA_ENVIRONMENT.get_template('user/new.html')
        context = {
            'data': data,
        }
        self.response.write(template.render(context))

    @decorator.oauth_required
    def post(self):
        first_name = self.request.get('first_name')
        last_name = self.request.get('last_name')
        email = self.request.get('email')
        password1 = self.request.get('password1')
        password2 = self.request.get('password2')
        enterprise = self.request.get('enterprise')

        if password1 == password2:
            try:
	            new_user = UserModel()
	            new_user.first_name = first_name.lower()
	            new_user.last_name = last_name.lower()
	            new_user.email = email.lower()
	            new_user.password = base64.b64encode(password1)
	            new_user.enterprise = enterprise.lower()
	            new_user.put()
	            self.response.write("creado")
            except:
                self.response.write("Error")
        else:
            self.redirect('/admin/users/new')
