# -*- coding: utf-8 -*-
#!/usr/bin/env python


import webapp2
import logging
import json


from google.appengine.api import taskqueue


from app.models.email_model import EmailModel
from app.mailers.mail_client import EmailClient


class InputEmailHandler(webapp2.RequestHandler):

    """
    Entrada receptora de datos de email para enviar desde 
    el DTE de Azurian
    """

    def post(self):
        campaign_id = self.request.get('campaign_id')
        email = self.request.get('email')
        full_name = self.request.get('full_name')
        subject = self.request.get('subject')
        htmlBody = self.request.get('htmlBody')
        file1 = self.request.POST.get('file1', None)
        file2 = self.request.POST.get('file2', None)
        file3 = self.request.POST.get('file3', None)
        logging.info(self.request.headers)
        #logging.info(self.request.body)
        #logging.info(file1.filename)
        #logging.info(file1.file.read())
        if (campaign_id and email and subject and htmlBody):
            # Proceso de creación del objeto email
            e = EmailModel()
            result = e.search_email(email, campaign_id)
            if result == None:
                try:
                    # Evaluar adjuntos
                    if not file1 == None:
                        attach1 = {
                            'name': unicode(file1.filename).encode('utf-8'),
                            'data': str(file1.file.read())
                        }
                    else:
                        attach1 = None
                    if not file2 == None:
                        attach2 = {
                            'name': unicode(file2.filename).encode('utf-8'),
                            'data': str(file2.file.read())
                        }
                    else:
                        attach2 = None
                    if not file3 == None:
                        attach3 = {
                            'name': unicode(file3.filename).encode('utf-8'),
                            'data': str(file3.file.read())
                        }
                    else:
                        attach3 = None
                    # Iniciando el proceso de envío de correo
                    sg_email = EmailClient()
                    sg_email.send_sg_email(email, full_name, subject, htmlBody, campaign_id, attach1, attach2, attach3)
                    e.campaign_id = campaign_id
                    e.email = email
                    e.full_name = full_name
                    e.subject = subject
                    e.htmlBody = htmlBody
                    e.put()
                    self.response.write({'message': 'success'})
                except e:
                    logging.error(e)
                """
                context = {
                    'email': email,
                    'campaign_id': campaign_id,
                    'full_name': full_name,
                    'subject': subject,
                    'htmlBody': htmlBody,
                }
                if not file1 == None:
                    context['file1'] = {
                        'name': unicode(file1.filename).encode('utf-8'),
                        'data': str(file1.file.read())
                    }
                else:
                    context['file1'] = None
                if not file2 == None:
                    context['file2'] = {
                        'name': unicode(file2.filename).encode('utf-8'),
                        'data': str(file2.file.read())
                    }
                else:
                    context['file2'] = None
                if not file3 == None:
                    context['file3'] = {
                        'name': unicode(file3.filename).encode('utf-8'),
                        'data': str(file3.file.read())
                    }
                else:
                    context['file3'] = None
                # Inicio taskqueue
                q = taskqueue.Queue('InputQueue')
                t = taskqueue.Task(url='/inputqueue', params=context)
                q.add(t)
                """
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
        self.response.write("Imprimiendo BODY desde la cola...")
        logging.info(self.request.body)
        """
        campaign_id = self.request.get('campaign_id')
        email = self.request.get('email')
        full_name = self.request.get('full_name')
        subject = self.request.get('subject')
        htmlBody = self.request.get('htmlBody')
        file1 = self.request.POST.get('file1', None)
        file2 = self.request.POST.get('file2', None)
        file3 = self.request.POST.get('file3', None)
        # Proceso de creación del objeto email
        e = EmailModel()
        result = e.search_email(email, campaign_id)
        if result == None:
            e.campaign_id = campaign_id
            e.email = email
            e.full_name = full_name
            e.subject = subject
            e.htmlBody = htmlBody
            e.put()
            # Iniciando el proceso de envío de correo
            sg_email = EmailClient()
            sg_email.send_sg_email(email, full_name, subject, htmlBody, campaign_id, file1, file2, file3)
        else:
            logging.info('objeto ya existe')
        """
