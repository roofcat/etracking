# encoding: utf-8
#!/usr/bin/env python


import webapp2
import json
import logging
import base64
import re


from app.models.email import EmailModel
from app.models.email import AttachModel


from config.jinja_environment import JINJA_ENVIRONMENT


class TestHandler(webapp2.RequestHandler):

    def get(self):
        total_count = len(EmailModel.query().fetch())
        total_processed = len(
            EmailModel.query(EmailModel.processed_event == 'processed').fetch())
        total_delivered = len(
            EmailModel.query(EmailModel.delivered_event == 'delivered').fetch())
        total_opened = len(
            EmailModel.query(EmailModel.opened_event == 'open').fetch())
        total_dropped = len(
            EmailModel.query(EmailModel.dropped_event == 'dropped').fetch())
        total_bounce = len(
            EmailModel.query(EmailModel.bounce_event == 'bounce').fetch())
        context = {
            'total_count': total_count,
            'total_processed': total_processed,
            'total_delivered': total_delivered,
            'total_opened': total_opened,
            'total_dropped': total_dropped,
            'total_bounce': total_bounce,
        }
        self.response.write(json.dumps(context))


class Test2Handler(webapp2.RequestHandler):

    def get(self):
        fallidos = EmailModel.query(EmailModel.processed_event == None).fetch()
        self.response.write(len(fallidos))
        self.response.write(
            "<br>----------------------------------------------<br>")
        for f in fallidos:
            self.response.write(f)
            self.response.write(
                "<br>----------------------------------------------<br>")


class Test3Handler(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('test/index.html')
        self.response.write(template.render())


class Test4Handler(webapp2.RequestHandler):

    def get(self):
        todo = EmailModel.query(group_by=['input_date'], projection=['input_date'], distinct=True).count()
        self.response.write(json.dumps(todo))


class Test5Handler(webapp2.RequestHandler):
    pass


class TestInputWithUserAndPassword(webapp2.RequestHandler):

    def get(self):
        logging.info(self.request.headers)
        logging.info(self.request.body)
        headers = self.request.headers
        auth = headers['Authorization']
        logging.info(auth)
        auth = re.sub('^Basic ', '', auth)
        user, password = base64.decodestring(auth).split(':')
        logging.info(user)
        logging.info(password)
