# -*- coding: utf-8 -*-
#!/usr/bin/env python


import datetime
import json
import logging


from app_controller import BaseHandler
from app.models.email import EmailModel
from app.models.email import JSONEncoder
from config.jinja_environment import JINJA_ENVIRONMENT


class CustomSearchHandler(BaseHandler):
    """ Ctrlr que trae el html de las busquedas personalizadas """

    def get(self):
        user = None
        try:
            user = self.session['user']
        except:
            self.redirect('/login/')
        if user:
            context = {'data': user, }
            template = JINJA_ENVIRONMENT.get_template(
                'customsearch/index.html')
            self.response.write(template.render(context))


class EmailSearchHandler(BaseHandler):

    def get(self, date_from, date_to, correo):
        if date_from and date_to and correo:
            # parametros de la url
            date_from = int(date_from)
            date_to = int(date_to)
            date_from = datetime.datetime.fromtimestamp(date_from)
            date_to = datetime.datetime.fromtimestamp(date_to)
            correo = str(correo).lower()
            # parametros de datatables
            sEcho = self.request.get('sEcho')
            sEcho = int(sEcho, base=10)
            iDisplayStart = self.request.get('iDisplayStart')
            iDisplayStart = int(iDisplayStart, base=10)
            iDisplayLength = self.request.get('iDisplayLength')
            iDisplayLength = int(iDisplayLength, base=10)
            # hacer la consulta
            query = EmailModel.get_info_by_email(date_from, date_to, correo,
                                                 display_start=iDisplayStart, display_length=iDisplayLength)
            context = {
                'sEcho': sEcho,
                'data': JSONEncoder().default(query['data']),
                'iTotalDisplayRecords': query['query_total'],
                'iTotalRecords': query['query_total'],
            }
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps(context))
        else:
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps({'message': 'error'}))


class FolioSearchHandler(BaseHandler):

    def get(self, folio):
        if folio:
            folio = str(folio)
            # parametros de datatables
            sEcho = self.request.get('sEcho')
            sEcho = int(sEcho, base=10)
            iDisplayStart = self.request.get('iDisplayStart')
            iDisplayStart = int(iDisplayStart, base=10)
            iDisplayLength = self.request.get('iDisplayLength')
            iDisplayLength = int(iDisplayLength, base=10)
            # hacer la consulta
            query = EmailModel.get_emails_by_folio(folio, 
                display_start=iDisplayStart, display_length=iDisplayLength)
            context = {
                'sEcho': sEcho,
                'data': JSONEncoder().default(query['data']),
                'iTotalDisplayRecords': query['query_total'],
                'iTotalRecords': query['query_total'],
            }
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps(context))
        else:
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps({'message': 'error'}))


class RutReceptorSearchHandler(BaseHandler):

    def get(self, date_from, date_to, rut):
        if date_from and date_to and rut:
            date_from = int(date_from)
            date_to = int(date_to)
            date_from = datetime.datetime.fromtimestamp(date_from)
            date_to = datetime.datetime.fromtimestamp(date_to)
            rut = str(rut)
            # parametros de datatables
            sEcho = self.request.get('sEcho')
            sEcho = int(sEcho, base=10)
            iDisplayStart = self.request.get('iDisplayStart')
            iDisplayStart = int(iDisplayStart, base=10)
            iDisplayLength = self.request.get('iDisplayLength')
            iDisplayLength = int(iDisplayLength, base=10)
            # hacer la consulta
            query = EmailModel.get_emails_by_rut_receptor(
                date_from, date_to, rut,
                display_start=iDisplayStart, display_length=iDisplayLength)
            context = {
                'sEcho': sEcho,
                'data': JSONEncoder().default(query['data']),
                'iTotalDisplayRecords': query['query_total'],
                'iTotalRecords': query['query_total'],
            }
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps(context))
        else:
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps({'message': 'error'}))


class FallidosSearchHandler(BaseHandler):

    def get(self, date_from, date_to):
        if date_from and date_to:
            date_from = int(date_from)
            date_to = int(date_to)
            date_from = datetime.datetime.fromtimestamp(date_from)
            date_to = datetime.datetime.fromtimestamp(date_to)
            # parametros de datatables
            sEcho = self.request.get('sEcho')
            sEcho = int(sEcho, base=10)
            iDisplayStart = self.request.get('iDisplayStart')
            iDisplayStart = int(iDisplayStart, base=10)
            iDisplayLength = self.request.get('iDisplayLength')
            iDisplayLength = int(iDisplayLength, base=10)
            # hacer la consulta
            query = EmailModel.get_all_failure_emails_by_dates(
                date_from, date_to, 
                display_start=iDisplayStart, display_length=iDisplayLength)
            context = {
                'sEcho': sEcho,
                'data': JSONEncoder().default(query['data']),
                'iTotalDisplayRecords': query['query_total'],
                'iTotalRecords': query['query_total'],
            }
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps(context))
        else:
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps({'message': 'error'}))


class MontosSearchHandler(BaseHandler):

    def get(self, date_from, date_to, mount_from, mount_to):
        if date_from and date_to and date_from and date_to:
            date_from = int(date_from, base=10)
            date_to = int(date_to, base=10)
            date_from = datetime.datetime.fromtimestamp(date_from)
            date_to = datetime.datetime.fromtimestamp(date_to)
            mount_from = int(mount_from, base=10)
            mount_to = int(mount_to, base=10)
            # parametros de datatables
            sEcho = self.request.get('sEcho')
            sEcho = int(sEcho, base=10)
            iDisplayStart = self.request.get('iDisplayStart')
            iDisplayStart = int(iDisplayStart, base=10)
            iDisplayLength = self.request.get('iDisplayLength')
            iDisplayLength = int(iDisplayLength, base=10)
            # hacer la consulta
            query = EmailModel.get_emails_by_mount(
                date_from, date_to, mount_from, mount_to,
                display_start=iDisplayStart, display_length=iDisplayLength)
            context = {
                'sEcho': sEcho,
                'data': JSONEncoder().default(query['data']),
                'iTotalDisplayRecords': query['query_total'],
                'iTotalRecords': query['query_total'],
            }
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps(context))
        else:
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps({'message': 'error'}))
