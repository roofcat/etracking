# -*- coding: utf-8 -*-
#!/usr/bin/env python


import logging


from sendgrid import SendGridClient
from sendgrid import Mail


from config.sendgrid import SG_API_KEY
from config.sendgrid import SG_API_USER
from config.sendgrid import SG_API_PASS
from config.sendgrid import SG_FROM
from config.sendgrid import SG_FROM_NAME


from app.models.email import AttachModel


class EmailClient(object):

    def __init__(self):
        self.sg = SendGridClient(SG_API_KEY)
        self.message = Mail()
        self.message.set_from(SG_FROM)
        self.message.set_from_name(SG_FROM_NAME)

    def send_sg_email(self, to, to_name, subject, html, campaign_id, enterprise, attachs=None):
        # valores de envío
        self.message.add_to(to)
        self.message.add_to_name(to_name)
        self.message.set_subject(subject)
        self.message.set_html(html)
        self.message.set_unique_args({'campaign_id': campaign_id, 'enterprise': enterprise})
        # Validacion de adjuntos
        if not attachs == None:
            for attach in attachs:
                att = AttachModel.query(ancestor=attach).get()
                self.message.add_attachment_stream(att.name, att.attach)
        # enviando el mail
        status, msg = self.sg.send(self.message)
        # imprimiendo respuesta
        logging.info(status)
        logging.info(msg)
