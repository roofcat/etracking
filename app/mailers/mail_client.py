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

    def send_sg_email(self, correo):
        # valores de envío
        self.message.add_to(correo.correo)
        self.message.add_to_name(correo.nombre_cliente)
        self.message.set_subject(correo.asunto)
        self.message.set_html(correo.html)
        # valores personalizados
        unique_args = {
            'empresa': correo.empresa,
            'rut_receptor': correo.rut_receptor,
            'rut_emisor': correo.rut_emisor,
            'tipo_envio': correo.tipo_envio,
            'tipo_dte': correo.tipo_dte,
            'numero_folio': correo.numero_folio,
            'resolucion_receptor': correo.resolucion_receptor,
            'resolucion_emisor': correo.resolucion_emisor,
            'monto': correo.monto,
            'fecha_emision': correo.fecha_emision,
            'fecha_recepcion': correo.fecha_recepcion,
            'estado_documento': correo.estado_documento,
            'tipo_operacion': correo.tipo_operacion,
            'tipo_receptor': correo.tipo_receptor,
        }
        self.message.set_unique_args(unique_args)
        # Validacion de adjuntos
        if correo.attachs:
            for adjunto in correo.attachs:
                adj = AttachModel.query(ancestor=adjunto).get()
                self.message.add_attachment_stream(adj.nombre, adj.archivo)
        # enviando el mail
        status, msg = self.sg.send(self.message)
        # imprimiendo respuesta
        logging.info(status)
        logging.info(msg)
