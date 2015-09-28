# -*- coding: utf-8 -*-
#!/usr/bin/env python


import logging
import datetime
import StringIO
import csv


from app_controller import BaseHandler
from app.models.user import UserModel
from app.models.email import EmailModel


class ExportGeneralEmailHandler(BaseHandler):

	def get(self, date_from, date_to, options):
		
		if date_from and date_to and options:
			try:
				date_from = int(date_from, base=10)
				date_to = int(date_to, base=10)
				date_from = datetime.datetime.fromtimestamp(date_from)
				date_to = datetime.datetime.fromtimestamp(date_to)
				# Consulta
				query = EmailModel.get_all_emails_by_dates(date_from, date_to, options)
				create_csv(self, query)
			except Exception, e:
				logging.info(e)


class ExportSendedEmailHandler(BaseHandler):

	def get(self, date_from, date_to, options):

		if date_from and date_to and options:
			try:
				date_from = int(date_from, base=10)
				date_to = int(date_to, base=10)
				date_from = datetime.datetime.fromtimestamp(date_from)
				date_to = datetime.datetime.fromtimestamp(date_to)
				# Consulta
				query = EmailModel.get_all_sended_emails_by_dates(date_from, date_to, options)
				create_csv(self, query)
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
				query = EmailModel.get_all_failure_emails_by_dates(date_from, date_to, options)
				create_csv(self, query)
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
				create_csv(self, query)
			except Exception, e:
				logging.info(e)


class ExportSearchByFolioHandler(BaseHandler):

	def get(self, folio):
		if folio:
			try:
				folio = int(folio, base=10)
				query = EmailModel.get_emails_by_folio(folio)
				create_csv(self, query)
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
				query = EmailModel.get_emails_by_rut_receptor(date_from, date_to, rut)
				create_csv(self, query)
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
				query = EmailModel.get_all_failure_emails_by_dates(date_from, date_to)
				create_csv(self, query)
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
				data = EmailModel.get_emails_by_mount(date_from, date_to, mount_from, mount_to)
				create_csv(self, query)
			except Exception, e:
				logging.info(e)


def create_csv(self, data):
	""" Función que crea un archivo CSV recibiendo como parametro
		un arreglo de objetos de una query al EmailModel """
	output = StringIO.StringIO()
	csv_out = csv.writer(output)

	# Cabecera del CSV
	csv_header = ['datetime', 'fecha_entrada', 'empresa', 'rut_receptor',
		'rut_emisor', 'tipo_envio', 'tipo_dte', 'numero_folio', 'resolucion_receptor',
		'resolucion_emisor', 'monto', 'fecha_emision', 'fecha_recepcion',
		'estado_documento', 'tipo_operacion', 'tipo_receptor', 'nombre_cliente',
		'correo', 'asunto', 'html', 'smtp_id', 'fecha_procesado', 'procesado',
		'fecha_envio', 'enviado', 'respuesta_envio', 'fecha_primera_lectura', 
		'fecha_ultima_lectura', 'abierto', 'ip_lector', 'navegador_lectura', 
		'cantidad_lectura', 'fecha_drop', 'razon_drop', 'drop', 'fecha_rebote', 
		'rebote', 'motivo_rebote', 'estado_Rebote', 'tipo_rebote', 
		'fecha_unsubscribe', 'unsubscribe_purchase', 'unsubscribe_id', 
		'unsubscribe', 'click_ip', 'click_purchase', 'click_navegador', 
		'click_event', 'click_email', 'fecha_click', 'click_url', ]
	# Escribir la cabecera en el CSV
	csv_out.writerow(csv_header)

	# Recorrer la consulta y armar row de cada registro
	for row in data:
		input_datetime = str(row.input_datetime)
		input_date = str(row.input_date)
		if row.empresa:
			empresa = row.empresa
		else:
			empresa = ''
		if row.rut_receptor:
			rut_receptor = row.rut_receptor
		else:
			rut_receptor = ''
		if row.rut_emisor:
			rut_emisor = row.rut_emisor
		else:
			rut_emisor = ''
		if row.tipo_envio:
			tipo_envio = row.tipo_envio
		else:
			tipo_envio = ''
		if row.tipo_dte:
			tipo_dte = row.tipo_dte
		else:
			tipo_dte = ''
		if row.numero_folio:
			numero_folio = row.numero_folio
		else:
			numero_folio = ''
		if row.resolucion_receptor:
			resolucion_receptor = row.resolucion_receptor
		else:
			resolucion_receptor = ''
		if row.resolucion_emisor:
			resolucion_emisor = row.resolucion_emisor
		else:
			resolucion_emisor = ''
		if row.monto:
			monto = row.monto
		else:
			monto = 0
		if row.fecha_emision:
			fecha_emision = row.fecha_emision
		else:
			fecha_emision = ''
		if row.fecha_recepcion:
			fecha_recepcion = row.fecha_recepcion
		else:
			fecha_recepcion = ''
		if row.estado_documento:
			estado_documento = row.estado_documento
		else:
			estado_documento = ''
		if row.tipo_operacion:
			tipo_operacion = row.tipo_operacion
		else:
			tipo_operacion = ''
		if row.tipo_receptor:
			tipo_receptor = row.tipo_receptor
		else:
			tipo_receptor = ''
		if row.nombre_cliente:
			nombre_cliente = row.nombre_cliente
		else:
			nombre_cliente = ''
		if row.correo:
			correo = row.correo
		else:
			correo = ''
		if row.asunto:
			asunto = row.asunto
		else:
			asunto = ''
		if row.html:
			html = row.html
		else:
			html = ''
		smtp_id = row.smtp_id
		processed_date = row.processed_date
		processed_event = row.processed_event
		delivered_date = row.delivered_date
		delivered_event = row.delivered_event
		delivered_response = row.delivered_response
		opened_first_date = row.opened_first_date
		opened_last_date = row.opened_last_date
		opened_event = row.opened_event
		opened_ip = row.opened_ip
		if row.opened_user_agent:
			opened_user_agent = str(row.opened_user_agent).replace(',', ' ').replace(';', ' ')
		else:
			opened_user_agent = ''
		opened_count = row.opened_count
		dropped_date = row.dropped_date
		if row.dropped_reason:
			dropped_reason = str(row.dropped_reason).replace(',', ' ').replace(';', ' ')
		else:
			dropped_reason = ''
		dropped_event = row.dropped_event
		bounce_date = row.bounce_date
		bounce_event = row.bounce_event
		if row.bounce_reason:
			bounce_reason = str(row.bounce_reason).replace(',', ' ').replace(';', ' ')
		else:
			bounce_reason = ''
		bounce_status = row.bounce_status
		bounce_type = row.bounce_type
		unsubscribe_date = row.unsubscribe_date
		unsubscribe_purchase = row.unsubscribe_purchase
		unsubscribe_id = row.unsubscribe_id
		unsubscribe_event = row.unsubscribe_event
		click_ip = row.click_ip
		click_purchase = row.click_purchase
		if row.click_useragent:
			click_useragent = str(row.click_useragent).replace(',', ' ').replace(';', ' ')
		else:
			click_useragent = ''
		click_event = row.click_event
		click_email = row.click_email
		click_date = row.click_date
		click_url = row.click_url

		csv_row = [input_datetime, input_date, empresa, rut_receptor, rut_emisor, 
		tipo_envio, tipo_dte, numero_folio, resolucion_receptor, resolucion_emisor, 
		monto, fecha_emision, fecha_recepcion, estado_documento, tipo_operacion, 
		tipo_receptor, nombre_cliente, correo, asunto, html, smtp_id, processed_date, 
		processed_event, delivered_date, delivered_event, delivered_response, 
		opened_first_date, opened_last_date, opened_event, opened_ip, opened_user_agent, 
		opened_count, dropped_date, dropped_reason, dropped_event, bounce_date, 
		bounce_event, bounce_reason, bounce_status, bounce_type, unsubscribe_date, 
		unsubscribe_purchase, unsubscribe_id, unsubscribe_event, click_ip, click_purchase, 
		click_useragent, click_event, click_email, click_date, click_url,]
		csv_out.writerow(csv_row)
	self.response.headers['Content-Type'] = 'text/csv'
	self.response.headers['Content-Disposition'] = 'attachment; filename=reporte.csv'
	content = output.getvalue()
	output.close()
	self.response.out.write(content)
