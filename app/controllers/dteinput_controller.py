# encoding: utf-8
#!/usr/bin/env python


import webapp2
import urllib2
import logging


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
        #attachments = [Attachment(attach.filename, attach.file.read())]

        if (campaign_id and email and subject and htmlBody):
            context = {
                'email': email,
                'campaign_id': campaign_id,
                'full_name': full_name,
                'subject': subject,
                'htmlBody': htmlBody,
            }
            q = taskqueue.Queue('InputQueue')
            t = taskqueue.Task(url='/inputqueue', params=context)
            q.add(t)
            self.response.write({'message': 'success'})
        else:
            self.response.write({'message': 'error fields'})


class InputEmailQueueHandler(webapp2.RequestHandler):

    """
    Entrada de ejecución definitiva del proceso de envío de correo
    """

    def post(self):
        campaign_id = self.request.get('campaign_id')
        email = self.request.get('email')
        full_name = self.request.get('full_name')
        subject = self.request.get('subject')
        htmlBody = self.request.get('htmlBody')

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
            sg_email.send_sg_email(email, full_name, subject, htmlBody, campaign_id)
        else:
            logging.info('objeto ya existe')
