# -*- coding: utf-8 -*-
#!/usr/bin/env python


import base64
import json
import datetime
import logging


from app_controller import BaseHandler
from app.models.user import UserModel
from app.models.email import EmailModel
from config.jinja_environment import JINJA_ENVIRONMENT


class DashboardHandler(BaseHandler):

    def get(self):
        user = None
        try:
            user = self.session['user']
        except:
            self.redirect('/login/')
        if user:
            context = { 'data': user,}
            template = JINJA_ENVIRONMENT.get_template('panel/index.html')
            self.response.write(template.render(context))


class CustomSearchHandler(BaseHandler):
    
    def get(self):
        user = None
        try:
            user = self.session['user']
        except:
            self.redirect('/login/')
        if user:
            context = { 'data': user, }
            template = JINJA_ENVIRONMENT.get_template('panel/custom_search.html')
            self.response.write(template.render(context))


class EmailPanelHandler(BaseHandler):

    def get(self):
        user = None
        try:
            user = self.session['user']
        except:
            self.redirect('/login/')
        if user:
            context = {
                'data': user,
            }
            template = JINJA_ENVIRONMENT.get_template('panel/email.html')
            self.response.write(template.render(context))

    def post(self):
        user = None
        try:
            user = self.session['user']
        except:
            self.redirect('/login/')
        correo = self.request.get('correo')
        correos = EmailModel.get_info_by_email(correo)
        context = {
            'data': user,
            'correos': correos,
        }
        template = JINJA_ENVIRONMENT.get_template('panel/email.html')
        self.response.write(template.render(context))


class FolioPanelHandler(BaseHandler):

    def get(self):
        user = None
        try:
            user = self.session['user']
        except:
            self.redirect('/login/')
        if user:
            context = {
                'data': user,
            }
            template = JINJA_ENVIRONMENT.get_template('panel/folio.html')
            self.response.write(template.render(context))

    def post(self):
        user = None
        try:
            user = self.session['user']
        except:
            self.redirect('/login/')
        folio = self.request.get('folio')
        correos = EmailModel.get_emails_by_folio(folio)
        context = {
            'data': user,
            'correos': correos,
        }
        template = JINJA_ENVIRONMENT.get_template('panel/folio.html')
        self.response.write(template.render(context))


class RutReceptorPanelHandler(BaseHandler):

    def get(self):
        user = None
        try:
            user = self.session['user']
        except:
            self.redirect('/login/')
        if user:
            context = {
                'data': user,
            }
            template = JINJA_ENVIRONMENT.get_template('panel/rut_receptor.html')
            self.response.write(template.render(context))

    def post(self):
        user = None
        try:
            user = self.session['user']
        except:
            self.redirect('/login/')
        rut = self.request.get('rut')
        correos = EmailModel.get_emails_by_rut_receptor(rut)
        context = {
            'data': user,
            'correos': correos,
        }
        template = JINJA_ENVIRONMENT.get_template('panel/rut_receptor.html')
        self.response.write(template.render(context))


class StatisticEmailPanelHandler(BaseHandler):

    def get(self):
        correo = self.request.get('correo')
        logging.info(correo)
        data = EmailModel.get_info_by_email(correo)
        context = {
            'data': data,
        }
        #logging.info(context)
        self.response.write(context)


class StatisticPanelHandler(BaseHandler):

    def get(self, date_from, date_to, options):

        if date_from and date_to and options:
            date_from = int(date_from)
            date_to = int(date_to)
            date_from = datetime.datetime.fromtimestamp(date_from)
            date_to = datetime.datetime.fromtimestamp(date_to)
            # busqueda de datos
            data = EmailModel.get_statistic_by_dates(date_from, date_to, options)
            results = EmailModel.get_stats_by_dates(date_from, date_to, options)
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
