# -*- coding: utf-8 -*-
#!/usr/bin/env python


import datetime
import json
import logging


from google.appengine.api import taskqueue
from google.appengine.ext import ndb
import webapp2


from app_controller import BaseHandler
from app.models.email import EmailModel
from app.models.export import ExportModel
from app.models.user import UserModel


from config.global_config import REPORT_EXPORT_URL
from config.global_config import REPORT_HTML_MAIL
from config.global_config import REPORT_SUBJECT_MAIL


from lib.mail_client import EmailClient
from lib.tablib_export import create_tablib
from lib.tablib_export import create_tablib_async


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
			data = EmailModel.get_all_emails_by_dates_async(date_from, date_to, options)
		elif export_type == 'export_sended_email':
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
			data = EmailModel.get_all_sended_emails_by_dates_async(date_from, date_to, options)
		elif export_type == 'export_failure_email':
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
			data = EmailModel.get_all_failure_emails_by_dates_async(date_from, date_to, options)
		elif export_type == 'export_search_by_email':
			email = self.request.get('email')
			email = str(email).lower()
			user_email = self.request.get('user_email')
			file_name = self.request.get('file_name')
			date_from = self.request.get('date_from')
			date_to = self.request.get('date_to')
			date_from = int(date_from, base=10)
			date_to = int(date_to, base=10)
			date_from = datetime.datetime.fromtimestamp(date_from)
			date_to = datetime.datetime.fromtimestamp(date_to)
			# Consulta
			data = EmailModel.get_info_by_email_async(date_from, date_to, email)
		elif export_type == 'export_search_by_folio':
			folio = self.request.get('folio')
			folio = str(folio).lower()
			user_email = self.request.get('user_email')
			file_name = self.request.get('file_name')
			# Consulta
			data = EmailModel.get_emails_by_folio_async(folio)
		elif export_type == 'export_search_by_rut':
			rut = self.request.get('rut')
			rut = str(rut).upper()
			user_email = self.request.get('user_email')
			file_name = self.request.get('file_name')
			date_from = self.request.get('date_from')
			date_to = self.request.get('date_to')
			date_from = int(date_from, base=10)
			date_to = int(date_to, base=10)
			date_from = datetime.datetime.fromtimestamp(date_from)
			date_to = datetime.datetime.fromtimestamp(date_to)
			# Consulta
			data = EmailModel.get_emails_by_rut_receptor_async(date_from, date_to, rut)
		elif export_type == 'export_search_by_failure':
			user_email = self.request.get('user_email')
			file_name = self.request.get('file_name')
			date_from = self.request.get('date_from')
			date_to = self.request.get('date_to')
			date_from = int(date_from, base=10)
			date_to = int(date_to, base=10)
			date_from = datetime.datetime.fromtimestamp(date_from)
			date_to = datetime.datetime.fromtimestamp(date_to)
			# Consulta
			data = EmailModel.get_all_failure_emails_by_dates_async(date_from, date_to)
		elif export_type == 'export_search_by_mount':
			mount_from = self.request.get('mount_from')
			mount_to = self.request.get('mount_to')
			mount_from = int(mount_from, base=10)
			mount_to = int(mount_to, base=10)
			user_email = self.request.get('user_email')
			file_name = self.request.get('file_name')
			date_from = self.request.get('date_from')
			date_to = self.request.get('date_to')
			date_from = int(date_from, base=10)
			date_to = int(date_to, base=10)
			date_from = datetime.datetime.fromtimestamp(date_from)
			date_to = datetime.datetime.fromtimestamp(date_to)
			# Consulta
			data = EmailModel.get_emails_by_mount_async(date_from, date_to, mount_from, mount_to)
		# Creación del documento
		doc_export = create_tablib_async(data)
		# Buscar el objeto usuario
		user = UserModel.get_user(user_email)
		logging.info(user)
		# Proceso de correo
		mail = EmailClient()
		mail_report = {
			'email': user.email,
			'user_name': user.first_name,
			'subject': REPORT_SUBJECT_MAIL,
			'html': REPORT_HTML_MAIL.format(user_name=user.first_name),
			'attach': {
				'name': file_name,
				'file': doc_export.xlsx,
			},
		}
		mail.send_mail_to_user_attach(mail_report)


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
			self.response.write(json.dumps({'status': 'ok'}))
		else:
			self.response.write(json.dumps({'status': 'no'}))


class ExportSendedEmailHandler(BaseHandler):

	def get(self, date_from, date_to, options):
		if date_from and date_to and options:
			user = self.session['user']
			context = {
				'date_from': int(date_from, base=10),
				'date_to': int(date_to, base=10),
				'options': options,
				'user_email': user['email'],
				'file_name': 'reporte_enviados.xlsx',
				'export_type': 'export_sended_email',
			}
			# Inicio taskqueue
			q = taskqueue.Queue('ReportQueue')
			t = taskqueue.Task(url='/exportqueue', params=context)
			q.add(t)
			self.response.write(json.dumps({'status': 'ok'}))
		else:
			self.response.write(json.dumps({'status': 'no'}))


class ExportFailureEmailHandler(BaseHandler):

	def get(self, date_from, date_to, options):
		if date_from and date_to and options:
			user = self.session['user']
			context = {
				'date_from': int(date_from, base=10),
				'date_to': int(date_to, base=10),
				'options': options,
				'user_email': user['email'],
				'file_name': 'reporte_fallidos.xlsx',
				'export_type': 'export_failure_email',
			}
			# Inicio taskqueue
			q = taskqueue.Queue('ReportQueue')
			t = taskqueue.Task(url='/exportqueue', params=context)
			q.add(t)
			self.response.write(json.dumps({'status': 'ok'}))
		else:
			self.response.write(json.dumps({'status': 'no'}))


class ExportSearchByEmailHandler(BaseHandler):

	def get(self, date_from, date_to, email):
		if date_from and date_to and email:
			user = self.session['user']
			context = {
				'date_from': int(date_from, base=10),
				'date_to': int(date_to, base=10),
				'email': email,
				'user_email': user['email'],
				'file_name': 'reporte_por_email.xlsx',
				'export_type': 'export_search_by_email',
			}
			# Inicio taskqueue
			q = taskqueue.Queue('ReportQueue')
			t = taskqueue.Task(url='/exportqueue', params=context)
			q.add(t)
			self.response.write(json.dumps({'status': 'ok'}))
		else:
			self.response.write(json.dumps({'status': 'no'}))


class ExportSearchByFolioHandler(BaseHandler):

	def get(self, folio):
		if folio:
			user = self.session['user']
			context = {
				'folio': str(folio),
				'user_email': user['email'],
				'file_name': 'reporte_por_folio.xlsx',
				'export_type': 'export_search_by_folio',
			}
			# Inicio taskqueue
			q = taskqueue.Queue('ReportQueue')
			t = taskqueue.Task(url='/exportqueue', params=context)
			q.add(t)
			self.response.write(json.dumps({'status': 'ok'}))
		else:
			self.response.write(json.dumps({'status': 'no'}))


class ExportSearchByRutHandler(BaseHandler):

	def get(self, date_from, date_to, rut):
		if date_from and date_to and rut:
			user = self.session['user']
			context = {
				'date_from': int(date_from, base=10),
				'date_to': int(date_to, base=10),
				'rut': rut,
				'user_email': user['email'],
				'file_name': 'reporte_por_rut.xlsx',
				'export_type': 'export_search_by_rut',
			}
			# Inicio taskqueue
			q = taskqueue.Queue('ReportQueue')
			t = taskqueue.Task(url='/exportqueue', params=context)
			q.add(t)
			self.response.write(json.dumps({'status': 'ok'}))
		else:
			self.response.write(json.dumps({'status': 'no'}))


class ExportSearchByFailureHandler(BaseHandler):

	def get(self, date_from, date_to):
		if date_from and date_to:
			user = self.session['user']
			context = {
				'date_from': int(date_from, base=10),
				'date_to': int(date_to, base=10),
				'user_email': user['email'],
				'file_name': 'reporte_fallidos.xlsx',
				'export_type': 'export_search_by_failure',
			}
			# Inicio taskqueue
			q = taskqueue.Queue('ReportQueue')
			t = taskqueue.Task(url='/exportqueue', params=context)
			q.add(t)
			self.response.write(json.dumps({'status': 'ok'}))
		else:
			self.response.write(json.dumps({'status': 'no'}))


class ExportSearchByMountHandler(BaseHandler):

	def get(self, date_from, date_to, mount_from, mount_to):
		if date_from and date_to:
			user = self.session['user']
			context = {
				'date_from': int(date_from, base=10),
				'date_to': int(date_to, base=10),
				'mount_from': int(mount_from, base=10),
				'mount_to': int(mount_to, base=10),
				'user_email': user['email'],
				'file_name': 'reporte_por_monto.xlsx',
				'export_type': 'export_search_by_mount',
			}
			# Inicio taskqueue
			q = taskqueue.Queue('ReportQueue')
			t = taskqueue.Task(url='/exportqueue', params=context)
			q.add(t)
			self.response.write(json.dumps({'status': 'ok'}))
		else:
			self.response.write(json.dumps({'status': 'no'}))
