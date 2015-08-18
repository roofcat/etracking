# -*- coding: utf-8 -*-
#!/usr/bin/env python


import logging


from app_controller import BaseHandler
from app.models.user import UserModel
from app.models.email import EmailModel


class ExportHomePanelHandler(BaseHandler):

	def get(self):
		date_from = self.request.get('date_from')
		date_to = self.request.get('date_to')
		options = self.request.get('options')

		if date_from and date_to and options:
			# Consulta
			query = EmailModel.get_all_emails_by_dates()
			create_csv(query)

	def create_csv(self, data):
		""" Función que crea un archivo CSV recibiendo como parametro
			un arreglo de objetos de una query al EmailModel """
		output = StringIO.StringIO()
		csv_out = csv.writer(output)

		# Cabecera del CSV
		csv_header = ['input_datetime', 'input_date', 'empresa', 'rut_receptor',
			'rut_emisor', 'tipo_envio', 'tipo_dte', 'numero_folio', 'resolucion_receptor',
			'resolucion_emisor', 'monto', 'fecha_emision', 'fecha_recepcion',
			'estado_documento', 'tipo_operacion', 'tipo_receptor', 'nombre_cliente',
			'correo', 'asunto', 'html', 'smtp_id', 'processed_date', 'processed_event',
			'processed_sg_event_id', 'processed_sg_message_id', 'delivered_date',
			'delivered_event', 'delivered_sg_event_id', 'delivered_sg_message_id',
			'delivered_response', 'opened_first_date', 'opened_last_date', 'opened_event',
			'opened_ip', 'opened_user_agent', 'opened_sg_event_id', 'opened_sg_message_id',
			'opened_count', 'dropped_date', 'dropped_sg_event_id', 'dropped_sg_message_id',
			'dropped_reason', 'dropped_event', 'bounce_date', 'bounce_event',
			'bounce_sg_event_id', 'bounce_sg_message_id', 'bounce_reason', 'bounce_status',
			'bounce_type', 'unsubscribe_date', 'unsubscribe_uid', 'unsubscribe_purchase',
			'unsubscribe_id', 'unsubscribe_event', 'click_ip', 'click_purchase',
			'click_useragent', 'click_event', 'click_email', 'click_date', 'click_url', ]
		# Escribir la cabecera en el CSV
		csv_out.writerow(csv_header)

		# Recorrer la consulta y armar row de cada registro
		for row in data:
			input_datetime = str(row.input_datetime)
			input_date = str(row.input_date)
			empresa = row.empresa
			rut_receptor = row.rut_receptor
			rut_emisor = row.rut_emisor
			tipo_envio = row.tipo_envio
			tipo_dte = row.tipo_dte
			numero_folio = row.numero_folio
			resolucion_receptor = row.resolucion_receptor
			resolucion_emisor = row.resolucion_emisor
			monto = row.monto
			fecha_emision = row.fecha_emision
			fecha_recepcion = row.fecha_recepcion
			estado_documento = row.estado_documento
			tipo_operacion = row.tipo_operacion
			tipo_receptor = row.tipo_receptor
			nombre_cliente = row.nombre_cliente
			correo = row.correo
			asunto = row.asunto
			html = row.html
			smtp_id = row.smtp_id
			processed_date = row.processed_date
			processed_event = row.processed_event
			processed_sg_event_id = row.processed_sg_event_id
			processed_sg_message_id = row.processed_sg_message_id
			delivered_date = row.delivered_date
			delivered_event = row.delivered_event
			delivered_sg_event_id = row.delivered_sg_event_id
			delivered_sg_message_id = row.delivered_sg_message_id
			delivered_response = row.delivered_response
			opened_first_date = row.opened_first_date
			opened_last_date = row.opened_last_date
			opened_event = row.opened_event
			opened_ip = row.opened_ip
			opened_user_agent = row.opened_user_agent
			opened_sg_event_id = row.opened_sg_event_id
			opened_sg_message_id = row.opened_sg_message_id
			opened_count = row.opened_count
			dropped_date = row.dropped_date
			dropped_sg_event_id = row.dropped_sg_event_id
			dropped_sg_message_id = row.dropped_sg_message_id
			dropped_reason = row.dropped_reason
			dropped_event = row.dropped_event
			bounce_date = row.bounce_date
			bounce_event = row.bounce_event
			bounce_sg_event_id = row.bounce_sg_event_id
			bounce_sg_message_id = row.bounce_sg_message_id
			bounce_reason = row.bounce_reason
			bounce_status = row.bounce_status
			bounce_type = row.bounce_type
			unsubscribe_date = row.unsubscribe_date
			unsubscribe_uid = row.unsubscribe_uid
			unsubscribe_purchase = row.unsubscribe_purchase
			unsubscribe_id = row.unsubscribe_id
			unsubscribe_event = row.unsubscribe_event
			click_ip = row.click_ip
			click_purchase = row.click_purchase
			click_useragent = row.click_useragent
			click_event = row.click_event
			click_email = row.click_email
			click_date = row.click_date
			click_url = row.click_url

			csv_row = [input_datetime, input_date, empresa, rut_receptor, rut_emisor,
			tipo_envio, tipo_dte, numero_folio, resolucion_receptor, resolucion_emisor,
			monto, fecha_emision, fecha_recepcion, estado_documento, tipo_operacion,
			tipo_receptor, nombre_cliente, correo, asunto, html, smtp_id, processed_date,
			processed_event, processed_sg_event_id, processed_sg_message_id, delivered_date,
			delivered_event, delivered_sg_event_id, delivered_sg_message_id,
			delivered_response, opened_first_date, opened_last_date, opened_event,
			opened_ip, opened_user_agent, opened_sg_event_id, opened_sg_message_id,
			opened_count, dropped_date, dropped_sg_event_id, dropped_sg_message_id,
			dropped_reason, dropped_event, bounce_date, bounce_event, bounce_sg_event_id,
			bounce_sg_message_id, bounce_reason, bounce_status, bounce_type, unsubscribe_date,
			unsubscribe_uid, unsubscribe_purchase, unsubscribe_id, unsubscribe_event,
			click_ip, click_purchase, click_useragent, click_event, click_email, click_date,
			click_url, ]
			csv_out.writerow(csv_row)
		self.response.headers['Content-Type'] = 'text/csv'
		self.response.headers['Content-Disposition'] = 'attachment; filename=file_export.csv'
		content = output.getvalue()
		output.close()
		self.response.out.write(content)
