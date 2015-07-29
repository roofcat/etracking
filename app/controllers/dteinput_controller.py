# -*- coding: utf-8 -*-
#!/usr/bin/env python


import webapp2
import logging


from google.appengine.api import taskqueue
from google.appengine.ext import blobstore


from app.models.email import EmailModel
from app.models.email import AttachModel
from app.mailers.mail_client import EmailClient


class InputEmailHandler(webapp2.RequestHandler):

    """ Entrada receptora de datos de email para enviar desde
        el DTE de Azurian
    """

    def post(self):
        # registro de header y body del request
        logging.info(self.request.headers)
        logging.info(self.request.body)
        # seteo de parametros recibidos
        empresa = self.request.get('empresa')
        rut_receptor = self.request.get('rut_receptor')
        rut_emisor = self.request.get('rut_emisor')
        tipo_envio = self.request.get('tipo_envio')
        tipo_dte = self.request.get('tipo_dte')
        numero_folio = self.request.get('numero_folio')
        resolucion_receptor = self.request.get('resolucion_receptor')
        resolucion_emisor = self.request.get('resolucion_emisor')
        monto = self.request.get('monto')
        fecha_emision = self.request.get('fecha_emision')
        fecha_recepcion = self.request.get('fecha_recepcion')
        estado_documento = self.request.get('estado_documento')
        tipo_operacion = self.request.get('tipo_operacion')
        tipo_receptor = self.request.get('tipo_receptor')
        nombre_cliente = self.request.get('nombre_cliente')
        correo = self.request.get('correo')
        asunto = self.request.get('asunto')
        html = self.request.get('html')
        # seteo de adjuntos si es que lo hubiera
        adjunto1 = self.request.POST.get('adjunto1', None)
        adjunto2 = self.request.POST.get('adjunto2', None)
        adjunto3 = self.request.POST.get('adjunto3', None)

        if (correo and asunto and html and numero_folio and tipo_dte):
            # Proceso de creación del objeto email
            my_email = EmailModel()
            email_result = my_email.search_email(
                correo, numero_folio, tipo_dte)
            if email_result == None:
                try:
                    my_email.empresa = empresa
                    my_email.rut_receptor = rut_receptor
                    my_email.rut_emisor = rut_emisor
                    my_email.tipo_envio = tipo_envio
                    my_email.tipo_dte = tipo_dte
                    my_email.numero_folio = numero_folio
                    my_email.resolucion_receptor = resolucion_receptor
                    my_email.resolucion_emisor = resolucion_emisor
                    my_email.monto = monto
                    my_email.fecha_emision = fecha_emision
                    my_email.fecha_recepcion = fecha_recepcion
                    my_email.estado_documento = estado_documento
                    my_email.tipo_operacion = tipo_operacion
                    my_email.tipo_receptor = tipo_receptor
                    my_email.nombre_cliente = nombre_cliente
                    my_email.correo = correo
                    my_email.asunto = asunto
                    my_email.html = html
                    # Evaluar adjuntos
                    if not adjunto1 == None:
                        att = AttachModel(
                            name=adjunto1.filename, attach=adjunto1.file.read()).put()
                        my_email.attachs.append(att)
                    if not adjunto2 == None:
                        att = AttachModel(
                            name=adjunto2.filename, attach=adjunto2.file.read()).put()
                        my_email.attachs.append(att)
                    if not adjunto3 == None:
                        att = AttachModel(
                            name=adjunto3.filename, attach=adjunto3.file.read()).put()
                        my_email.attachs.append(att)
                    my_email.put()
                    context = {
                        'correo': correo,
                        'numero_folio': numero_folio,
                        'tipo_dte': tipo_dte,
                    }
                    # Inicio taskqueue
                    q = taskqueue.Queue('InputQueue')
                    t = taskqueue.Task(url='/inputqueue', params=context)
                    q.add(t)
                    self.response.write({'message': 'success'})
                except Exception, e:
                    logging.error(e)
            else:
                logging.info('objeto ya existe')
            # fin todo
        else:
            self.response.write({'message': 'error fields'})


class InputEmailQueueHandler(webapp2.RequestHandler):

    """ Entrada de ejecución definitiva del proceso de envío de correo """

    def post(self):
        correo = self.request.get('correo')
        numero_folio = self.request.get('numero_folio')
        tipo_dte = self.request.get('tipo_dte')
        # Valicacion de datos
        if (correo, numero_folio, tipo_dte):
            # Proceso de creación del objeto email
            my_email = EmailModel()
            email_result = my_email.search_email(
                correo, numero_folio, tipo_dte)
            if not email_result == None:
                # Iniciando el proceso de envío de correo
                sg_email = EmailClient()
                sg_email.send_sg_email(email_result)
            else:
                logging.info('Correo no existe')
        else:
            logging.error("PARAMETROS INCORRECTOS")
