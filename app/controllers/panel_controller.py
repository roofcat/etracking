# -*- coding: utf-8 -*-
#!/usr/bin/env python


import base64
import json
import datetime


from app_controller import BaseHandler
from app.models.user import UserModel
from app.models.email import EmailModel
from config.oauth2_utils import decorator
from config.oauth2_utils import user_info_service
from config.jinja_environment import JINJA_ENVIRONMENT


class HomePanelHandler(BaseHandler):

    def get(self):
        user = None
        try:
            user = self.session['user']
        except:
            self.redirect('/login')
        if user:
            context = {
                'data': user,
            }
            template = JINJA_ENVIRONMENT.get_template('panel/index.html')
            self.response.write(template.render(context))


class StatisticPanelHandler(BaseHandler):

    def get(self):
        date_from = self.request.get('date_from')
        date_to = self.request.get('date_to')

        if date_from and date_to:
            # preparacion de parametros
            date_from = int(date_from)
            date_to = int(date_to)
            date_from = datetime.datetime.fromtimestamp(date_from)
            date_to = datetime.datetime.fromtimestamp(date_to)
            # busqueda de datos
            data = EmailModel.get_statistic_by_dates(date_from, date_to)
            results = EmailModel.get_stats_by_dates(date_from, date_to)
            context = {
                'date_from': str(date_from),
                'date_to': str(date_to),
                'statistic': data,
                'results': results,
            }
            self.response.write(json.dumps(context))


class LoginPanelHandler(BaseHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('panel/login.html')
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
                self.response.write("Clave incorrecta")


class LogoutPanelHandler(BaseHandler):

    def get(self):
        try:
            del self.session['user']
        except:
            pass
        self.redirect('/')
