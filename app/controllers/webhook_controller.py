# -*- coding: utf-8 -*-
#!/usr/bin/env python


import logging
import webapp2
import json
import datetime


from app.models.email_model import EmailModel


class SendrigWebhookHandler(webapp2.RequestHandler):

    def post(self):
        """
        Metodo que recibe los eventos generados al intentar enviar correos a SendGrid
        Los eventos capturados son (procesado, enviado, abierto, descartado, rebotado)
        """
        # se captura y se parsea a json el body del request recibido por el
        # webhook
        request_body = json.loads(self.request.body)

        for body in request_body:
            """
            Evaluar el tipo de evento ya que trae campos diferentes
            """
            logging.info(request_body)

            event = str(body['event'])
            email = str(body['email'])
            campaign_id = str(body['campaign_id'])
            enterprise = str(body['enterprise'])

            logging.info(event)

            if event and email and campaign_id:
                
                if event == 'processed':
                    # instanciar objeto EmailModel
                    e = EmailModel()
                    email_model = e.search_email(enterprise, email, campaign_id)

                    if not email_model == None:
                        email_model.smtp_id = body['smtp-id']
                        email_model.procesed_date = datetime.datetime.fromtimestamp(
                            body['timestamp'])
                        email_model.procesed_event = event
                        email_model.procesed_sg_event_id = body['sg_event_id']
                        email_model.procesed_sg_message_id = body[
                            'sg_message_id']
                        email_model.put()

                elif event == 'delivered':
                    # instanciar objeto EmailModel
                    e = EmailModel()
                    email_model = e.search_email(enterprise, email, campaign_id)

                    if not email_model == None:
                        email_model.smtp_id = body['smtp-id']
                        email_model.delivered_date = datetime.datetime.fromtimestamp(
                            body['timestamp'])
                        email_model.delivered_event = event
                        email_model.delivered_sg_event_id = body['sg_event_id']
                        email_model.delivered_sg_message_id = body[
                            'sg_message_id']
                        email_model.delivered_response = body['response']
                        email_model.put()

                elif event == 'open':
                    # instanciar objeto EmailModel
                    e = EmailModel()
                    email_model = e.search_email(enterprise, email, campaign_id)

                    if not email_model == None:
                        if email_model.opened_first_date == None:
                            email_model.opened_first_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        email_model.opened_last_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        email_model.opened_event = event
                        email_model.opened_ip = body['ip']
                        email_model.opened_user_agent = body['useragent']
                        email_model.opened_sg_event_id = body['sg_event_id']
                        email_model.opened_sg_message_id = body[
                            'sg_message_id']
                        #email_model.opened_count = ndb.IntegerProperty(default=0)
                        e.email_add_count(email_model)
                        email_model.put()

                elif event == 'dropped':
                    # instanciar objeto EmailModel
                    e = EmailModel()
                    email_model = e.search_email(enterprise, email, campaign_id)

                    if not email_model == None:
                        email_model.smtp_id = body['smtp-id']
                        email_model.dropped_date = datetime.datetime.fromtimestamp(
                            body['timestamp'])
                        email_model.dropped_sg_event_id = body['sg_event_id']
                        email_model.dropped_sg_message_id = body[
                            'sg_message_id']
                        email_model.dropped_reason = body['reason']
                        email_model.dropped_event = event
                        email_model.put()

                elif event == 'bounce':
                    # instanciar objeto EmailModel
                    e = EmailModel()
                    email_model = e.search_email(enterprise, email, campaign_id)

                    if not email_model == None:
                        email_model.smtp_id = body['smtp-id']
                        email_model.bounce_date = datetime.datetime.fromtimestamp(
                            body['timestamp'])
                        email_model.bounce_event = event
                        email_model.bounce_sg_event_id = body['sg_event_id']
                        email_model.bounce_sg_message_id = body[
                            'sg_message_id']
                        email_model.bounce_reason = body['reason']
                        email_model.bounce_status = body['status']
                        email_model.bounce_type = body['type']
                        email_model.put()
                elif event == 'unsubscribe':
                    e = EmailModel()
                    email_model = e.search_email(enterprise, email, campaign_id)

                    if not email_model == None:
                        email_model.unsubscribe_date = body['timestamp']
                        email_model.unsubscribe_uid = body['uid']
                        email_model.unsubscribe_purchase = body['purchase']
                        email_model.unsubscribe_id = body['id']
                        email_model.unsubscribe_event = body['event']
                        email_model.put()
            else:
                logging.info('body con campos vacios')
