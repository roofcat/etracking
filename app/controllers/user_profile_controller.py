# -*- coding: utf-8 -*-
#!/usr/bin/env python


import base64
import datetime
import logging


from app_controller import BaseHandler
from app.models.user import UserModel
from config.jinja_environment import JINJA_ENVIRONMENT


class ProfilePanelHandler(BaseHandler):

    def get(self):
        user = None
        user = self.session['user']
        context = { 'data': user, }
        template = JINJA_ENVIRONMENT.get_template('user/profile.html')
        self.response.write(template.render(context))


class UpdateProfilePanelHandler(BaseHandler):

    def get(self):
        user = None
        user = self.session['user']
        first_name = self.request.get('first_name')
        last_name = self.request.get('last_name')
        if first_name and last_name:
            update_user = UserModel.get_user(user['email'])
            update_user.first_name = first_name
            update_user.last_name = last_name
            update_user.put()
            session_user = {
                'first_name': update_user.first_name,
                'last_name': update_user.last_name,
                'email': update_user.email,
                'is_admin': update_user.is_admin,
                'enterprise': update_user.enterprise,
                'is_custom_user': update_user.is_custom_user,
            }
            self.session['user'] = session_user
            self.response.write({'response': 'ok'})
        else:
            self.response.write({'response': 'fail'})


class UpdatePasswordProfilePanelHandler(BaseHandler):

    def get(self):
        user = None
        user = self.session['user']
        first_name = self.request.get('first_name')
        last_name = self.request.get('last_name')
        if first_name and last_name:
            update_user = UserModel.get_user(user['email'])
            update_user.first_name = first_name
            update_user.last_name = last_name
            update_user.put()
            session_user = {
                'first_name': update_user.first_name,
                'last_name': update_user.last_name,
                'email': update_user.email,
                'is_admin': update_user.is_admin,
                'enterprise': update_user.enterprise,
                'is_custom_user': update_user.is_custom_user,
            }
            self.session['user'] = session_user
            self.response.write({'response': 'ok'})
        else:
            self.response.write({'response': 'fail'})


class LoginPanelHandler(BaseHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('user/login.html')
        self.response.write(template.render())

    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')

        current_user = UserModel()

        if email and password:
            password = base64.b64encode(password)
            this_user = current_user.get_user(email)
            if this_user.password == password:
                user = {
                    'first_name': this_user.first_name,
                    'last_name': this_user.last_name,
                    'email': this_user.email,
                    'is_admin': this_user.is_admin,
                    'enterprise': this_user.enterprise,
                    'is_custom_user': this_user.is_custom_user,
                }
                self.session['user'] = user
                self.redirect('/')
            else:
                self.redirect('/login/')
        else:
            self.redirect('/login/')


class LogoutPanelHandler(BaseHandler):

    def get(self):
        try:
            del self.session['user']
        except:
            pass
        self.redirect('/')
