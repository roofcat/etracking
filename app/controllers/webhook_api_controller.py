# -*- coding: utf-8 -*-
#!/usr/bin/env python

""" Este controlador sirve para recibir los webhook
    generados por SendGrid para los correos enviados
    utilizando la API SendGrid (Java, Python, etc)
    que el cliente haya implementado en su DTE.
"""


import logging
import webapp2
import json
import datetime


from app.models.email import EmailModel


class SendgridWebhookAPIHandler(webapp2.RequestHandler):

    def post(self):
        """ Metodo que recibe los eventos generados al intentar enviar correos a SendGrid
        Los eventos capturados son (procesado, enviado, abierto, descartado, rebotado) """
        # se captura y se parsea a json el body del request recibido por el
        # webhook
        request_body = json.loads(self.request.body)

        for body in request_body:
            """ Evaluar el tipo de evento ya que trae campos diferentes """
            logging.info(request_body)

            event = str(body['event'])
            correo = str(body['email'])
            numero_folio = str(body['numero_folio'])
            tipo_dte = str(body['tipo_dte'])

            logging.info(event)

            if event and correo and numero_folio and tipo_dte:

                if event == 'processed':
                    email_model = EmailModel.search_email(correo, numero_folio, tipo_dte)
                    if not email_model == None:
                        email_model.smtp_id = body['smtp-id']
                        email_model.processed_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        email_model.processed_event = event
                        email_model.processed_sg_event_id = body['sg_event_id']
                        email_model.processed_sg_message_id = body['sg_message_id']
                        email_model.correo = str(body['email'])
                        email_model.numero_folio = str(body['numero_folio'])
                        email_model.tipo_dte = str(body['tipo_dte'])
                        email_model.put()
                    else:
                        e = EmailModel()
                        e.smtp_id = body['smtp-id']
                        e.processed_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        e.processed_event = event
                        e.processed_sg_event_id = body['sg_event_id']
                        e.processed_sg_message_id = body['sg_message_id']
                        e.correo = str(body['email'])
                        e.numero_folio = str(body['numero_folio'])
                        e.tipo_dte = str(body['tipo_dte'])
                        e.put()

                elif event == 'delivered':
                    email_model = EmailModel.search_email(correo, numero_folio, tipo_dte)
                    if not email_model == None:
                        email_model.smtp_id = body['smtp-id']
                        email_model.delivered_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        email_model.delivered_event = event
                        email_model.delivered_sg_event_id = body['sg_event_id']
                        email_model.delivered_sg_message_id = body['sg_message_id']
                        email_model.delivered_response = body['response']
                        email_model.correo = str(body['email'])
                        email_model.numero_folio = str(body['numero_folio'])
                        email_model.tipo_dte = str(body['tipo_dte'])
                        email_model.put()
                    else:
                        e = EmailModel()
                        e.smtp_id = body['smtp-id']
                        e.delivered_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        e.delivered_event = event
                        e.delivered_sg_event_id = body['sg_event_id']
                        e.delivered_sg_message_id = body['sg_message_id']
                        e.delivered_response = body['response']
                        e.correo = str(body['email'])
                        e.numero_folio = str(body['numero_folio'])
                        e.tipo_dte = str(body['tipo_dte'])
                        e.put()

                elif event == 'open':
                    model = EmailModel()
                    email_model = EmailModel.search_email(correo, numero_folio, tipo_dte)
                    if not email_model == None:
                        if email_model.opened_first_date == None:
                            email_model.opened_first_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        email_model.opened_last_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        email_model.opened_event = event
                        email_model.opened_ip = body['ip']
                        email_model.opened_user_agent = body['useragent']
                        email_model.opened_sg_event_id = body['sg_event_id']
                        email_model.opened_sg_message_id = body['sg_message_id']
                        model.email_add_count(email_model)
                        email_model.correo = str(body['email'])
                        email_model.numero_folio = str(body['numero_folio'])
                        email_model.tipo_dte = str(body['tipo_dte'])
                        email_model.put()
                    else:
                        e = EmailModel()
                        if e.opened_first_date == None:
                            e.opened_first_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        e.opened_last_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        e.opened_event = event
                        e.opened_ip = body['ip']
                        e.opened_user_agent = body['useragent']
                        e.opened_sg_event_id = body['sg_event_id']
                        e.opened_sg_message_id = body['sg_message_id']
                        e.email_add_count(e)
                        e.correo = str(body['email'])
                        e.numero_folio = str(body['numero_folio'])
                        e.tipo_dte = str(body['tipo_dte'])
                        e.put()

                elif event == 'dropped':
                    email_model = EmailModel.search_email(correo, numero_folio, tipo_dte)
                    if not email_model == None:
                        email_model.smtp_id = body['smtp-id']
                        email_model.dropped_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        email_model.dropped_sg_event_id = body['sg_event_id']
                        email_model.dropped_sg_message_id = body['sg_message_id']
                        email_model.dropped_reason = body['reason']
                        email_model.dropped_event = event
                        email_model.correo = str(body['email'])
                        email_model.numero_folio = str(body['numero_folio'])
                        email_model.tipo_dte = str(body['tipo_dte'])
                        email_model.put()
                    else:
                        e = EmailModel()
                        e.smtp_id = body['smtp-id']
                        e.dropped_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        e.dropped_sg_event_id = body['sg_event_id']
                        e.dropped_sg_message_id = body['sg_message_id']
                        e.dropped_reason = body['reason']
                        e.dropped_event = event
                        e.correo = str(body['email'])
                        e.numero_folio = str(body['numero_folio'])
                        e.tipo_dte = str(body['tipo_dte'])
                        e.put()

                elif event == 'bounce':
                    email_model = EmailModel.search_email(correo, numero_folio, tipo_dte)
                    if not email_model == None:
                        email_model.bounce_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        email_model.bounce_event = event
                        email_model.bounce_sg_event_id = body['sg_event_id']
                        email_model.bounce_sg_message_id = body['sg_message_id']
                        email_model.bounce_reason = body['reason']
                        email_model.bounce_status = body['status']
                        email_model.bounce_type = body['type']
                        email_model.correo = str(body['email'])
                        email_model.numero_folio = str(body['numero_folio'])
                        email_model.tipo_dte = str(body['tipo_dte'])
                        email_model.put()
                    else:
                        e = EmailModel()
                        e.bounce_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        e.bounce_event = event
                        e.bounce_sg_event_id = body['sg_event_id']
                        e.bounce_sg_message_id = body['sg_message_id']
                        e.bounce_reason = str(body['reason']).decode("utf-8")
                        e.bounce_status = body['status']
                        e.bounce_type = body['type']
                        e.correo = str(body['email'])
                        e.numero_folio = str(body['numero_folio'])
                        e.tipo_dte = str(body['tipo_dte'])
                        e.put()

                elif event == 'unsubscribe':
                    email_model = EmailModel.search_email(correo, numero_folio, tipo_dte)
                    if not email_model == None:
                        email_model.unsubscribe_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        email_model.unsubscribe_uid = body['uid']
                        email_model.unsubscribe_purchase = body['purchase']
                        email_model.unsubscribe_id = body['id']
                        email_model.unsubscribe_event = body['event']
                        email_model.correo = str(body['email'])
                        email_model.numero_folio = str(body['numero_folio'])
                        email_model.tipo_dte = str(body['tipo_dte'])
                        email_model.put()
                    else:
                        e = EmailModel()
                        e.unsubscribe_date = datetime.datetime.fromtimestamp(body['timestamp'])
                        e.unsubscribe_uid = body['uid']
                        e.unsubscribe_purchase = body['purchase']
                        e.unsubscribe_id = body['id']
                        e.unsubscribe_event = body['event']
                        e.correo = str(body['email'])
                        e.numero_folio = str(body['numero_folio'])
                        e.tipo_dte = str(body['tipo_dte'])
                        e.put()
            else:
                logging.info('body con campos vacios')
