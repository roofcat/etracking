# -*- coding: utf-8 -*-
#!/usr/bin/env python


import logging
import StringIO
import csv
import codecs


def create_csv(self, data, file_name='reporte.csv'):
	""" Función que crea un archivo CSV recibiendo como parametro
		un arreglo de objetos de una query al EmailModel """
	output = StringIO.StringIO()
	csv.encoder = codecs.getincrementaldecoder('utf-8')()
	csv_out = csv.writer(output)

	# Cabecera del CSV
	csv_header = ['datetime', 'empresa', 'rut_receptor',
		'rut_emisor', 'tipo_envio', 'tipo_dte', 'numero_folio', 'resolucion_receptor',
		'resolucion_emisor', 'monto', 'fecha_emision', 'fecha_recepcion',
		'estado_documento', 'tipo_operacion', 'tipo_receptor', 'nombre_cliente',
		'correo', 'asunto', 'fecha_procesado', 'procesado',
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
	try:
		for row in data:
			logging.info(row)
			input_datetime = str(row.input_datetime)
			if row.empresa:
				empresa = unicode(row.empresa).encode('utf-8')
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
				nombre_cliente = unicode(row.nombre_cliente).encode('utf-8')
			else:
				nombre_cliente = ''
			if row.correo:
				correo = unicode(row.correo).encode('utf-8')
			else:
				correo = ''
			if row.asunto:
				asunto = unicode(row.asunto).encode('utf-8')
			else:
				asunto = ''
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

			csv_row = [input_datetime, empresa, rut_receptor, rut_emisor, 
			tipo_envio, tipo_dte, numero_folio, resolucion_receptor, resolucion_emisor, 
			monto, fecha_emision, fecha_recepcion, estado_documento, tipo_operacion, 
			tipo_receptor, nombre_cliente, correo, asunto, processed_date, 
			processed_event, delivered_date, delivered_event, delivered_response, 
			opened_first_date, opened_last_date, opened_event, opened_ip, opened_user_agent, 
			opened_count, dropped_date, dropped_reason, dropped_event, bounce_date, 
			bounce_event, bounce_reason, bounce_status, bounce_type, unsubscribe_date, 
			unsubscribe_purchase, unsubscribe_id, unsubscribe_event, click_ip, click_purchase, 
			click_useragent, click_event, click_email, click_date, click_url,]
			csv_out.writerow(csv_row)
		self.response.headers['Content-Type'] = 'text/csv'
		self.response.headers['Content-Disposition'] = 'attachment; filename=' + file_name
		content = output.getvalue()
		content = content.decode('utf-8')
		output.close()
		self.response.out.write(content)
	except Exception, e:
		logging.error(e)
