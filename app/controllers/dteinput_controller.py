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
    """
    Entrada receptora de datos de email para enviar desde
    el DTE de Azurian
    """
    def post(self):
        logging.info(self.request.headers)
        logging.info(self.request.body)
        enterprise = self.request.get('enterprise')
        campaign_id = self.request.get('campaign_id')
        email = self.request.get('email')
        recipient_type = self.request.get('recipient_type')
        full_name = self.request.get('full_name')
        subject = self.request.get('subject')
        htmlBody = self.request.get('htmlBody')
        file1 = self.request.POST.get('file1', None)
        file2 = self.request.POST.get('file2', None)
        file3 = self.request.POST.get('file3', None)
        if (enterprise and campaign_id and email and subject and htmlBody and recipient_type):
            # Proceso de creación del objeto email
            my_email = EmailModel()
            email_result = my_email.search_email(enterprise, email, campaign_id)
            if email_result == None:
                try:
                    my_email.enterprise = enterprise
                    my_email.campaign_id = campaign_id
                    my_email.email = email
                    my_email.recipient_type = recipient_type
                    my_email.full_name = full_name
                    my_email.subject = subject
                    my_email.htmlBody = htmlBody
                    # Evaluar adjuntos
                    if not file1 == None:
                        att = AttachModel(name=file1.filename, attach=file1.file.read()).put()
                        my_email.attachs.append(att)
                    if not file2 == None:
                        att = AttachModel(name=file2.filename, attach=file2.file.read()).put()
                        my_email.attachs.append(att)
                    if not file3 == None:
                        att = AttachModel(name=file3.filename, attach=file3.file.read()).put()
                        my_email.attachs.append(att)
                    my_email.put()
                    context = {
                        'enterprise': enterprise,
                        'campaign_id': campaign_id,
                        'email': email,
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
    """
    Entrada de ejecución definitiva del proceso de envío de correo
    """
    def post(self):
        enterprise = self.request.get('enterprise')
        campaign_id = self.request.get('campaign_id')
        email = self.request.get('email')
        # Valicacion de datos
        if (enterprise, campaign_id, email):
            # Proceso de creación del objeto email
            my_email = EmailModel()
            email_result = my_email.search_email(enterprise, email, campaign_id)
            if not email_result == None:
                # Iniciando el proceso de envío de correo
                sg_email = EmailClient()
                sg_email.send_sg_email(
                    email_result.email,
                    email_result.full_name,
                    email_result.subject,
                    email_result.htmlBody,
                    email_result.campaign_id,
                    email_result.enterprise,
                    email_result.attachs
                )
            else:
                logging.info('Correo no existe')
        else:
            logging.error("PARAMETROS INCORRECTOS")
