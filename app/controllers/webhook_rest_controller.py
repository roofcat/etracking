# -*- coding: utf-8 -*-
#!/usr/bin/env python

""" Este controlador sirve para recibir los webhook
    generados por SendGrid para los correos enviados
    utilizando la API Rest del Tracking.
"""


import logging
import webapp2
import json
import datetime


from app.models.email import EmailModel


class SendgridWebhookApiRestHandler(webapp2.RequestHandler):

    def post(self):
        """ Metodo que recibe los eventos generados al intentar enviar correos a SendGrid
        Los eventos capturados son (procesado, enviado, abierto, descartado, rebotado) """
        # se captura y se parsea a json el body del request recibido por el
        # webhook
        request_body = json.loads(self.request.body)

        for body in request_body:
            """ Evaluar el tipo de evento ya que trae campos diferentes """
            logging.info(request_body)

            event = str(body['event']).decode("utf-8")
            correo = str(body['email']).decode("utf-8")
            numero_folio = str(body['numero_folio']).decode("utf-8")
            tipo_dte = str(body['tipo_dte']).decode("utf-8")

            logging.info(event)

            if event and correo and numero_folio and tipo_dte:

                if event == 'processed':
                    # instanciar objeto EmailModel
                    e = EmailModel()
                    email_model = e.search_email(correo, numero_folio, tipo_dte)

                    if not email_model == None:
                        email_model.smtp_id = str(body['smtp-id']).decode('utf-8')
                        email_model.processed_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        email_model.processed_event = event
                        email_model.processed_sg_event_id = str(body['sg_event_id']).decode("utf-8")
                        email_model.processed_sg_message_id = str(body['sg_message_id']).decode("utf-8")
                        email_model.put()

                elif event == 'delivered':
                    # instanciar objeto EmailModel
                    e = EmailModel()
                    email_model = e.search_email(correo, numero_folio, tipo_dte)

                    if not email_model == None:
                        email_model.smtp_id = str(body['smtp-id']).decode('utf-8')
                        email_model.delivered_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        email_model.delivered_event = event
                        email_model.delivered_sg_event_id = str(body['sg_event_id']).decode("utf-8")
                        email_model.delivered_sg_message_id = str(body['sg_message_id']).decode("utf-8")
                        email_model.delivered_response = str(body['response']).decode("utf-8")
                        email_model.put()

                elif event == 'open':
                    # instanciar objeto EmailModel
                    e = EmailModel()
                    email_model = e.search_email(correo, numero_folio, tipo_dte)

                    if not email_model == None:
                        if email_model.opened_first_date == None:
                            email_model.opened_first_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        email_model.opened_last_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        email_model.opened_event = event
                        email_model.opened_ip = str(body['ip']).decode("utf-8")
                        email_model.opened_user_agent = str(body['useragent']).decode("utf-8")
                        email_model.opened_sg_event_id = str(body['sg_event_id']).decode("utf-8")
                        email_model.opened_sg_message_id = str(body['sg_message_id']).decode("utf-8")
                        e.email_add_count(email_model)
                        email_model.put()

                elif event == 'dropped':
                    # instanciar objeto EmailModel
                    e = EmailModel()
                    email_model = e.search_email(
                        correo, numero_folio, tipo_dte)

                    if not email_model == None:
                        email_model.smtp_id = str(body['smtp-id']).decode('utf-8')
                        email_model.dropped_date = datetime.datetime.fromtimestamp(
                            body['timestamp'])
                        email_model.dropped_sg_event_id = str(body['sg_event_id']).decode("utf-8")
                        email_model.dropped_sg_message_id = str(body['sg_message_id']).decode("utf-8")
                        email_model.dropped_reason = str(body['reason']).decode("utf-8")
                        email_model.dropped_event = event
                        email_model.put()

                elif event == 'bounce':
                    # instanciar objeto EmailModel
                    e = EmailModel()
                    email_model = e.search_email(correo, numero_folio, tipo_dte)

                    if not email_model == None:
                        email_model.smtp_id = str(body['smtp-id']).decode('utf-8')
                        email_model.bounce_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        email_model.bounce_event = event
                        email_model.bounce_sg_event_id = str(body['sg_event_id']).decode("utf-8")
                        email_model.bounce_sg_message_id = str(body['sg_message_id']).decode("utf-8")
                        email_model.bounce_reason = str(body['reason']).decode("utf-8")
                        email_model.bounce_status = str(body['status']).decode("utf-8")
                        email_model.bounce_type = str(body['type']).decode("utf-8")
                        email_model.put()

                elif event == 'unsubscribe':
                    e = EmailModel()
                    email_model = e.search_email(correo, numero_folio, tipo_dte)

                    if not email_model == None:
                        email_model.unsubscribe_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        email_model.unsubscribe_uid = str(body['uid']).decode("utf-8")
                        email_model.unsubscribe_purchase = str(body['purchase']).decode("utf-8")
                        email_model.unsubscribe_id = str(body['id']).decode("utf-8")
                        email_model.unsubscribe_event = str(body['event']).decode("utf-8")
                        email_model.put()
                elif event == 'click':
                    e = EmailModel()
                    email_model = e.search_email(correo, numero_folio, tipo_dte)

                    if not email_model == None:                        
                        email_model.click_ip = str(body['ip']).decode("utf-8")
                        email_model.click_purchase = str(body['purchase']).decode("utf-8")
                        email_model.click_useragent = str(body['useragent']).decode("utf-8")
                        email_model.click_event = str(body['event']).decode("utf-8")
                        email_model.click_email = str(body['email']).decode("utf-8")
                        email_model.click_date = body['timestamp']
                        email_model.click_url = str(body['url']).decode("utf-8")
                        email_model.put()
            else:
                logging.info('body con campos vacios')
