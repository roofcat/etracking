# -*- coding: utf-8 -*-
#!/usr/bin/env python


import datetime


from google.appengine.ext import ndb


tipos_de_receptor = ['dte', 'cliente', ]
tipos_de_envio = ['notificacion', 'aceptacion', 'rechazo', 'rems', ]
tipos_de_estados_documentos = [
    'recepcionado', 'no recepcionado', 'aceptado', 'rechazado', ]
tipos_de_operaciones = ['compra', 'venta', ]


class AttachModel(ndb.Model):
    nombre = ndb.StringProperty()
    archivo = ndb.BlobProperty()


class EmailModel(ndb.Model):
    # campos basicos
    input_datetime = ndb.DateTimeProperty(auto_now_add=True)
    input_date = ndb.DateProperty(auto_now_add=True)
    # campos dte
    empresa = ndb.StringProperty(required=True)
    rut_receptor = ndb.StringProperty(required=True)
    rut_emisor = ndb.StringProperty(required=True)
    tipo_envio = ndb.StringProperty(required=True, choices=tipos_de_envio)
    tipo_dte = ndb.StringProperty()
    numero_folio = ndb.StringProperty()
    resolucion_receptor = ndb.StringProperty()
    resolucion_emisor = ndb.StringProperty()
    monto = ndb.IntegerProperty()
    fecha_emision = ndb.DateProperty()
    fecha_recepcion = ndb.DateProperty()
    estado_documento = ndb.StringProperty(choices=tipos_de_estados_documentos)
    tipo_operacion = ndb.StringProperty(choices=tipos_de_operaciones)
    tipo_receptor = ndb.StringProperty(choices=tipos_de_receptor)
    # campos correo
    nombre_cliente = ndb.StringProperty(required=False)
    correo = ndb.StringProperty(required=True)
    asunto = ndb.StringProperty(required=True)
    html = ndb.TextProperty(required=True)
    # adjuntos
    #attachs = ndb.StructuredProperty(AttachModel, repeated=True)
    attachs = ndb.KeyProperty(kind='AttachModel', repeated=True)
    # campos de processed
    smtp_id = ndb.StringProperty()
    processed_date = ndb.DateTimeProperty()
    processed_event = ndb.StringProperty(indexed=True)
    processed_sg_event_id = ndb.StringProperty()
    processed_sg_message_id = ndb.StringProperty()
    # campos delivered
    delivered_date = ndb.DateTimeProperty()
    delivered_event = ndb.StringProperty(indexed=True)
    delivered_sg_event_id = ndb.StringProperty()
    delivered_sg_message_id = ndb.StringProperty()
    delivered_response = ndb.TextProperty()
    # campos open
    opened_first_date = ndb.DateTimeProperty()
    opened_last_date = ndb.DateTimeProperty()
    opened_event = ndb.StringProperty(indexed=True)
    opened_ip = ndb.StringProperty()
    opened_user_agent = ndb.StringProperty()
    opened_sg_event_id = ndb.StringProperty()
    opened_sg_message_id = ndb.StringProperty()
    opened_count = ndb.IntegerProperty(default=0)
    # campos dropped
    dropped_date = ndb.DateTimeProperty()
    dropped_sg_event_id = ndb.StringProperty()
    dropped_sg_message_id = ndb.StringProperty()
    dropped_reason = ndb.StringProperty()
    dropped_event = ndb.StringProperty(indexed=True)
    # campos bounce
    bounce_date = ndb.DateTimeProperty()
    bounce_event = ndb.StringProperty(indexed=True)
    bounce_sg_event_id = ndb.StringProperty()
    bounce_sg_message_id = ndb.StringProperty()
    bounce_reason = ndb.TextProperty()
    bounce_status = ndb.StringProperty()
    bounce_type = ndb.StringProperty()
    # campos unscribes
    unsubscribe_date = ndb.DateTimeProperty()
    unsubscribe_uid = ndb.StringProperty()
    unsubscribe_purchase = ndb.StringProperty()
    unsubscribe_id = ndb.StringProperty()
    unsubscribe_event = ndb.StringProperty(indexed=True)

    def search_email(self, correo, numero_folio, tipo_dte):
        """ Retorna el objeto para determinar si existe o no """
        return EmailModel.query(
            ndb.AND(
                EmailModel.correo == correo,
                EmailModel.numero_folio == numero_folio,
                EmailModel.tipo_dte == tipo_dte
            )).get()

    def email_add_count(self, data):
        """ Incrementa el campo de lecturas efectuadas 
            por el receptor del correo """
        data.opened_count = data.opened_count + 1
        data.put()

    @classmethod
    def get_stats_by_dates(self, from_date, to_date, tipo_receptor):
        # dias para restar
        day = datetime.timedelta(days=1)
        end_date = from_date
        # arreglo para armar el objeto de respuesta
        data_result = [
            ["Fecha", "Solicitudes", "Procesados", "Enviados",
                "Abiertos", "Rechazados", "Rebotados"]
        ]

        while end_date <= to_date:

            if tipo_receptor == 'all':
                query = EmailModel.query(EmailModel.input_date >= end_date,
                                         EmailModel.input_date <= end_date)
            else:
                query = EmailModel.query(EmailModel.input_date >= end_date,
                                         EmailModel.input_date <= end_date,
                                         EmailModel.tipo_receptor == tipo_receptor)
            total = query.count()
            processed = query.filter(
                EmailModel.processed_event == "processed").count()
            delivered = query.filter(
                EmailModel.delivered_event == "delivered").count()
            opened = query.filter(EmailModel.opened_event == "open").count()
            dropped = query.filter(
                EmailModel.dropped_event == "dropped").count()
            bounced = query.filter(EmailModel.bounce_event == "bounce").count()
            data = [
                str(end_date), total, processed, delivered, opened, dropped, bounced]
            data_result.append(data)
            end_date = end_date + day
        return data_result

    @classmethod
    def get_statistic_by_dates(self, from_date, to_date, tipo_receptor):

        if tipo_receptor == 'all':
            query = EmailModel.query(EmailModel.input_date >= from_date,
                                     EmailModel.input_date <= to_date)
        else:
            query = EmailModel.query(EmailModel.input_date >= from_date,
                                     EmailModel.input_date <= to_date,
                                     EmailModel.tipo_receptor == tipo_receptor)
        total = query.count()
        processed = query.filter(
            EmailModel.processed_event == "processed").count()
        delivered = query.filter(
            EmailModel.delivered_event == "delivered").count()
        opened = query.filter(EmailModel.opened_event == "open").count()
        dropped = query.filter(EmailModel.dropped_event == "dropped").count()
        bounced = query.filter(EmailModel.bounce_event == "bounce").count()
        return {
            'total': total,
            'processed': processed,
            'delivered': delivered,
            'opened': opened,
            'dropped': dropped,
            'bounced': bounced,
        }
