# -*- coding: utf-8 -*-
#!/usr/bin/env python


import codecs
import csv
import datetime
import logging
import StringIO
import webapp2


from google.appengine.api import taskqueue


from app_controller import BaseHandler
from app.mailers.mail_client import EmailClient
from app.models.email import EmailModel
from app.models.export import ExportModel
from app.models.user import UserModel


from config.global_config import REPORT_EXPORT_URL
from config.global_config import REPORT_SUBJECT_MAIL
from config.global_config import REPORT_HTML_MAIL


from lib.tablib_export import create_tablib


class QueueExportHandler(webapp2.RequestHandler):
    """ Clase manejadora de las colas de tareas
            para generar los documentos para reportes 
            y enviarlos como link al correo del usuario
    """

    def post(self):
        export_type = self.request.get('export_type')
        if export_type == 'export_general_email':
            options = self.request.get('options')
            user_email = self.request.get('user_email')
            file_name = self.request.get('file_name')
            date_from = self.request.get('date_from')
            date_to = self.request.get('date_to')
            date_from = int(date_from, base=10)
            date_to = int(date_to, base=10)
            date_from = datetime.datetime.fromtimestamp(date_from)
            date_to = datetime.datetime.fromtimestamp(date_to)
            # Consulta
            data = EmailModel.get_all_emails_by_dates(date_from, date_to, options)
            # Creación del documento
            doc_export = create_tablib(data)
            # Buscar el objeto usuario
            user = UserModel.get_user(user_email)
            # Creación de objeto reporte
            report = ExportModel()
            report.name = file_name
            report.export_file = doc_export.xlsx
            report.user = user.email
            report.put()
            # actualizar campo
            report.url = REPORT_EXPORT_URL.format(url_safe=report.key.urlsafe())
            report.put()
            # Proceso de correo
            mail = EmailClient()
            mail_report = {
                'email': user.email,
                'user_name': user.first_name,
                'subject': REPORT_SUBJECT_MAIL,
                'html': REPORT_HTML_MAIL.format(user_name=user.first_name, report_link=report.url),
            }
            mail.send_user_email(mail_report)
        elif export_type == '':
            pass
        elif export_type == '':
            pass
        elif export_type == '':
            pass
        elif export_type == '':
            pass


""" Serie de clases controladoras que reciben parametros
	para exportar documentos y enviarlo a la cola de tareas
	para que se generen y envíen los documentos por email
	con un link
"""


class ExportGeneralEmailHandler(BaseHandler):

	def get(self, date_from, date_to, options):
		if date_from and date_to and options:
			user = self.session['user']
			context = {
				'date_from': int(date_from, base=10),
				'date_to': int(date_to, base=10),
				'options': options,
				'user_email': user['email'],
				'file_name': 'reporte_general.xlsx',
				'export_type': 'export_general_email',
			}
			# Inicio taskqueue
			q = taskqueue.Queue('ReportQueue')
			t = taskqueue.Task(url='/exportqueue', params=context)
			q.add(t)


class ExportSendedEmailHandler(BaseHandler):

    def get(self, date_from, date_to, options):

        if date_from and date_to and options:
            try:
                date_from = int(date_from, base=10)
                date_to = int(date_to, base=10)
                date_from = datetime.datetime.fromtimestamp(date_from)
                date_to = datetime.datetime.fromtimestamp(date_to)
                # Consulta
                query = EmailModel.get_all_sended_emails_by_dates(
                    date_from, date_to, options)
                create_csv(self, query, 'reporte_enviados.csv')
            except Exception, e:
                logging.info(e)


class ExportFailureEmailHandler(BaseHandler):

    def get(self, date_from, date_to, options):

        if date_from and date_to and options:
            try:
                date_from = int(date_from, base=10)
                date_to = int(date_to, base=10)
                date_from = datetime.datetime.fromtimestamp(date_from)
                date_to = datetime.datetime.fromtimestamp(date_to)
                # Consulta
                query = EmailModel.get_all_failure_emails_by_dates(
                    date_from, date_to, options)
                create_csv(self, query, 'reporte_fallidos.csv')
            except Exception, e:
                logging.info(e)


class ExportSearchByEmailHandler(BaseHandler):

    def get(self, date_from, date_to, email):

        if date_from and date_to and email:
            try:
                date_from = int(date_from, base=10)
                date_to = int(date_to, base=10)
                date_from = datetime.datetime.fromtimestamp(date_from)
                date_to = datetime.datetime.fromtimestamp(date_to)
                email = str(email).lower()
                query = EmailModel.get_info_by_email(date_from, date_to, email)
                create_csv(self, query, 'reporte_por_email.csv')
            except Exception, e:
                logging.info(e)


class ExportSearchByFolioHandler(BaseHandler):

    def get(self, folio):
        if folio:
            try:
                folio = str(folio)
                query = EmailModel.get_emails_by_folio(folio)
                logging.info(query)
                create_csv(self, query, 'reporte_por_folio.csv')
            except Exception, e:
                logging.info(e)


class ExportSearchByRutHandler(BaseHandler):

    def get(self, date_from, date_to, rut):
        if date_from and date_to and rut:
            try:
                date_from = int(date_from, base=10)
                date_to = int(date_to, base=10)
                date_from = datetime.datetime.fromtimestamp(date_from)
                date_to = datetime.datetime.fromtimestamp(date_to)
                rut = str(rut).upper()
                query = EmailModel.get_emails_by_rut_receptor(
                    date_from, date_to, rut)
                create_csv(self, query, 'reporte_por_rut.csv')
            except Exception, e:
                logging.info(e)


class ExportSearchByFailureHandler(BaseHandler):

    def get(self, date_from, date_to):
        if date_from and date_to:
            try:
                date_from = int(date_from, base=10)
                date_to = int(date_to, base=10)
                date_from = datetime.datetime.fromtimestamp(date_from)
                date_to = datetime.datetime.fromtimestamp(date_to)
                query = EmailModel.get_all_failure_emails_by_dates(
                    date_from, date_to)
                create_csv(self, query, 'reporte_fallidos.csv')
            except Exception, e:
                logging.info(e)


class ExportSearchByMountHandler(BaseHandler):

    def get(self, date_from, date_to, mount_from, mount_to):
        if date_from and date_to:
            try:
                date_from = int(date_from, base=10)
                date_to = int(date_to, base=10)
                date_from = datetime.datetime.fromtimestamp(date_from)
                date_to = datetime.datetime.fromtimestamp(date_to)
                mount_from = int(mount_from, base=10)
                mount_to = int(mount_to, base=10)
                data = EmailModel.get_emails_by_mount(
                    date_from, date_to, mount_from, mount_to)
                create_csv(self, query, 'reporte_por_monto.csv')
            except Exception, e:
                logging.info(e)
