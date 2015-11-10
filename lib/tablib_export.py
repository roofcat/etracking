# -*- coding: utf-8 -*-
#!/usr/bin/env python


import datetime
import logging
import tablib
from google.appengine.ext import ndb


""" Esta función genera excel en tiempo real de ejecución 
    ya que recibe como parametro un arreglo de objetos
"""
def create_tablib(data):
    my_tab = tablib.Dataset()
    my_tab.headers = (
        'datetime', 'empresa', 'rut_receptor', 'rut_emisor', 'tipo_envio', 'tipo_dte', 
        'numero_folio', 'resolucion_receptor', 'resolucion_emisor', 'monto', 'fecha_emision', 
        'fecha_recepcion', 'estado_documento', 'tipo_operacion', 'tipo_receptor', 
        'nombre_cliente', 'correo', 'asunto', 'fecha_procesado', 'procesado', 'fecha_envio', 
        'enviado', 'respuesta_envio', 'fecha_primera_lectura', 'fecha_ultima_lectura', 
        'abierto', 'ip_lector', 'navegador_lectura', 'cantidad_lectura', 'fecha_drop', 
        'razon_drop', 'drop', 'fecha_rebote', 'rebote', 'motivo_rebote', 'estado_Rebote', 
        'tipo_rebote', 'fecha_unsubscribe', 'unsubscribe_purchase', 'unsubscribe_id', 
        'unsubscribe', 'click_ip', 'click_purchase', 'click_navegador', 'click_event', 
        'click_email', 'fecha_click', 'click_url'
    )
    if data:
        for row in data:
            input_datetime = row.input_datetime
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
                monto = ''
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
            if row.processed_date:
                processed_date = row.processed_date
            else:
                processed_date = ''
            if row.processed_event:
                processed_event = row.processed_event
            else:
                processed_event = ''
            if row.delivered_date:
                delivered_date = row.delivered_date
            else:
                delivered_date = ''
            if row.delivered_event:
                delivered_event = row.delivered_event
            else:
                delivered_event = ''
            if row.delivered_response:
                delivered_response = row.delivered_response
            else:
                delivered_response = ''
            if row.opened_first_date:
                opened_first_date = row.opened_first_date
            else:
                opened_first_date = ''
            if row.opened_last_date:
                opened_last_date = row.opened_last_date
            else:
                opened_last_date = ''
            if row.opened_event:
                opened_event = row.opened_event
            else:
                opened_event = ''
            if row.opened_ip:
                opened_ip = row.opened_ip
            else:
                opened_ip = ''
            if row.opened_user_agent:
                opened_user_agent = row.opened_user_agent
            else:
                opened_user_agent = ''
            if row.opened_count:
                opened_count = row.opened_count
            else:
                opened_count = ''
            if row.dropped_date:
                dropped_date = row.dropped_date
            else:
                dropped_date = ''
            if row.dropped_reason:
                dropped_reason = row.dropped_reason
            else:
                dropped_reason = ''
            if row.dropped_event:
                dropped_event = row.dropped_event
            else:
                dropped_event = ''
            if row.bounce_date:
                bounce_date = row.bounce_date
            else:
                bounce_date = ''
            if row.bounce_event:
                bounce_event = row.bounce_event
            else:
                bounce_event = ''
            if row.bounce_reason:
                bounce_reason = row.bounce_reason
            else:
                bounce_reason = ''
            if row.bounce_status:
                bounce_status = row.bounce_status
            else:
                bounce_status = ''
            if row.bounce_type:
                bounce_type = row.bounce_type
            else:
                bounce_type = ''
            if row.unsubscribe_date:
                unsubscribe_date = row.unsubscribe_date
            else:
                unsubscribe_date = ''
            if row.unsubscribe_purchase:
                unsubscribe_purchase = row.unsubscribe_purchase
            else:
                unsubscribe_purchase = ''
            if row.unsubscribe_id:
                unsubscribe_id = row.unsubscribe_id
            else:
                unsubscribe_id = ''
            if row.unsubscribe_event:
                unsubscribe_event = row.unsubscribe_event
            else:
                unsubscribe_event = ''
            if row.click_ip:
                click_ip = row.click_ip
            else:
                click_ip = ''
            if row.click_purchase:
                click_purchase = row.click_purchase
            else:
                click_purchase = ''
            if row.click_useragent:
                click_useragent = row.click_useragent
            else:
                click_useragent = ''
            if row.click_event:
                click_event = row.click_event
            else:
                click_event = ''
            if row.click_email:
                click_email = row.click_email
            else:
                click_email = ''
            if row.click_date:
                click_date = row.click_date
            else:
                click_date = ''
            if row.click_url:
                click_url = row.click_url
            else:
                click_url = ''
            xlsx_row = (
                input_datetime, empresa, rut_receptor, rut_emisor, tipo_envio, tipo_dte, 
                numero_folio, resolucion_receptor, resolucion_emisor, monto, fecha_emision, 
                fecha_recepcion, estado_documento, tipo_operacion, tipo_receptor, 
                nombre_cliente, correo, asunto, processed_date, processed_event, 
                delivered_date, delivered_event, delivered_response, opened_first_date, 
                opened_last_date, opened_event, opened_ip, opened_user_agent, opened_count, 
                dropped_date, dropped_reason, dropped_event, bounce_date, bounce_event, 
                bounce_reason, bounce_status, bounce_type, unsubscribe_date, 
                unsubscribe_purchase, unsubscribe_id, unsubscribe_event, click_ip, click_purchase, 
                click_useragent, click_event, click_email, click_date, click_url
            )
            my_tab.append(xlsx_row)
        return my_tab

""" Esta función genera excel en los procesos de colas de tareas
    en background ya que recibe un objeto "Future" de ndb datastore
    y es un iterable
"""
def create_tablib_async(data):
    my_tab = tablib.Dataset()
    my_tab.headers = (
        'datetime', 'empresa', 'rut_receptor', 'rut_emisor', 'tipo_envio', 'tipo_dte', 
        'numero_folio', 'resolucion_receptor', 'resolucion_emisor', 'monto', 'fecha_emision', 
        'fecha_recepcion', 'estado_documento', 'tipo_operacion', 'tipo_receptor', 
        'nombre_cliente', 'correo', 'asunto', 'fecha_procesado', 'procesado', 'fecha_envio', 
        'enviado', 'respuesta_envio', 'fecha_primera_lectura', 'fecha_ultima_lectura', 
        'abierto', 'ip_lector', 'navegador_lectura', 'cantidad_lectura', 'fecha_drop', 
        'razon_drop', 'drop', 'fecha_rebote', 'rebote', 'motivo_rebote', 'estado_Rebote', 
        'tipo_rebote', 'fecha_unsubscribe', 'unsubscribe_purchase', 'unsubscribe_id', 
        'unsubscribe', 'click_ip', 'click_purchase', 'click_navegador', 'click_event', 
        'click_email', 'fecha_click', 'click_url'
    )
    # evaluar si el objeto data es una
    # lista o un Future
    if isinstance(data, list):
        rows = data
    elif isinstance(data, ndb.Future):
        rows = data.get_result()
    if rows:
        # recorrer data
        for row in rows:
            input_datetime = row.input_datetime
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
                monto = ''
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
            if row.processed_date:
                processed_date = row.processed_date
            else:
                processed_date = ''
            if row.processed_event:
                processed_event = row.processed_event
            else:
                processed_event = ''
            if row.delivered_date:
                delivered_date = row.delivered_date
            else:
                delivered_date = ''
            if row.delivered_event:
                delivered_event = row.delivered_event
            else:
                delivered_event = ''
            if row.delivered_response:
                delivered_response = row.delivered_response
            else:
                delivered_response = ''
            if row.opened_first_date:
                opened_first_date = row.opened_first_date
            else:
                opened_first_date = ''
            if row.opened_last_date:
                opened_last_date = row.opened_last_date
            else:
                opened_last_date = ''
            if row.opened_event:
                opened_event = row.opened_event
            else:
                opened_event = ''
            if row.opened_ip:
                opened_ip = row.opened_ip
            else:
                opened_ip = ''
            if row.opened_user_agent:
                opened_user_agent = row.opened_user_agent
            else:
                opened_user_agent = ''
            if row.opened_count:
                opened_count = row.opened_count
            else:
                opened_count = ''
            if row.dropped_date:
                dropped_date = row.dropped_date
            else:
                dropped_date = ''
            if row.dropped_reason:
                dropped_reason = row.dropped_reason
            else:
                dropped_reason = ''
            if row.dropped_event:
                dropped_event = row.dropped_event
            else:
                dropped_event = ''
            if row.bounce_date:
                bounce_date = row.bounce_date
            else:
                bounce_date = ''
            if row.bounce_event:
                bounce_event = row.bounce_event
            else:
                bounce_event = ''
            if row.bounce_reason:
                bounce_reason = row.bounce_reason
            else:
                bounce_reason = ''
            if row.bounce_status:
                bounce_status = row.bounce_status
            else:
                bounce_status = ''
            if row.bounce_type:
                bounce_type = row.bounce_type
            else:
                bounce_type = ''
            if row.unsubscribe_date:
                unsubscribe_date = row.unsubscribe_date
            else:
                unsubscribe_date = ''
            if row.unsubscribe_purchase:
                unsubscribe_purchase = row.unsubscribe_purchase
            else:
                unsubscribe_purchase = ''
            if row.unsubscribe_id:
                unsubscribe_id = row.unsubscribe_id
            else:
                unsubscribe_id = ''
            if row.unsubscribe_event:
                unsubscribe_event = row.unsubscribe_event
            else:
                unsubscribe_event = ''
            if row.click_ip:
                click_ip = row.click_ip
            else:
                click_ip = ''
            if row.click_purchase:
                click_purchase = row.click_purchase
            else:
                click_purchase = ''
            if row.click_useragent:
                click_useragent = row.click_useragent
            else:
                click_useragent = ''
            if row.click_event:
                click_event = row.click_event
            else:
                click_event = ''
            if row.click_email:
                click_email = row.click_email
            else:
                click_email = ''
            if row.click_date:
                click_date = row.click_date
            else:
                click_date = ''
            if row.click_url:
                click_url = row.click_url
            else:
                click_url = ''
            xlsx_row = (
                input_datetime, empresa, rut_receptor, rut_emisor, tipo_envio, tipo_dte, 
                numero_folio, resolucion_receptor, resolucion_emisor, monto, fecha_emision, 
                fecha_recepcion, estado_documento, tipo_operacion, tipo_receptor, 
                nombre_cliente, correo, asunto, processed_date, processed_event, 
                delivered_date, delivered_event, delivered_response, opened_first_date, 
                opened_last_date, opened_event, opened_ip, opened_user_agent, opened_count, 
                dropped_date, dropped_reason, dropped_event, bounce_date, bounce_event, 
                bounce_reason, bounce_status, bounce_type, unsubscribe_date, 
                unsubscribe_purchase, unsubscribe_id, unsubscribe_event, click_ip, click_purchase, 
                click_useragent, click_event, click_email, click_date, click_url
            )
            my_tab.append(xlsx_row)
        logging.info("tipo my_tab")
        logging.info(type(my_tab))
        return my_tab
