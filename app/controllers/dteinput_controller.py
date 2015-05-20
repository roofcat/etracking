# -*- coding: utf-8 -*-
#!/usr/bin/env python


import webapp2
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
        logging.info(self.request.headers)
        logging.info(self.request.body)
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
                        attach1 = {'name': unicode(file1.filename).encode('utf-8'), 'data': str(file1.file.read())}
                    else:
                        attach1 = None
                    if not file2 == None:
                        attach2 = {'name': unicode(file2.filename).encode('utf-8'), 'data': str(file2.file.read())}
                    else:
                        attach2 = None
                    if not file3 == None:
                        attach3 = {'name': unicode(file3.filename).encode('utf-8'), 'data': str(file3.file.read())}
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
                except e:
                    logging.error(e)
            else:
                logging.info('objeto ya existe')
            """
            context = {
                'email': email,
                'campaign_id': campaign_id,
                'full_name': full_name,
                'subject': subject,
                'htmlBody': htmlBody,
                'file1': [file1.filename, file1.file.read()],
                'file2': file2,
                'file3': file3,
            }
            q = taskqueue.Queue('InputQueue')
            t = taskqueue.Task(url='/inputqueue', params=context)
            #t = taskqueue.Task(url='/inputqueue', payload=context)
            q.add(t)
            """
            self.response.write({'message': 'success'})
        else:
            self.response.write({'message': 'error fields'})


class InputEmailQueueHandler(webapp2.RequestHandler):

    """
    Entrada de ejecución definitiva del proceso de envío de correo
    """

    def post(self):
        pass
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
            sg_email.send_sg_email(email, full_name, subject, htmlBody, campaign_id, file1)
        else:
            logging.info('objeto ya existe')
        """
