# -*- coding: utf-8 -*-
#!/usr/bin/env python


from datetime import datetime, time, date, timedelta
import logging
import json


from google.appengine.ext import ndb


tipos_de_receptor = ['dte', 'cliente', ]
tipos_de_envio = ['notificacion', 'aceptacion', 'rechazo', 'rems', ]
tipos_de_estados_documentos = [
    'recepcionado', 'no recepcionado', 'aceptado', 'rechazado', ]
tipos_de_operaciones = ['compra', 'venta', ]


class JSONEncoder(json.JSONEncoder):

    def default(self, obj):
        simple_types = (int, long, float, bool, basestring)

        if isinstance(obj, ndb.Key):
            return obj.urlsafe()

        if isinstance(obj, ndb.Model):
            dct = obj.to_dict()
            dct['id'] = obj.key.id()
            return self.default(dct)

        if isinstance(obj, list):
            return [self.default(l) for l in obj]

        if isinstance(obj, dict):
            x = {}
            for l in obj:
                x[l] = self.default(obj[l])
            return x

        if isinstance(obj, simple_types):
            return unicode(obj)

        if obj is None:
            return ''

        if isinstance(obj, datetime):
            return unicode(datetime.strftime(obj, '%Y-%m-%d %H:%M:%S'))

        if isinstance(obj, date):
            return unicode(datetime.strftime(obj, '%Y-%m-%d'))

        if isinstance(obj, time):
            return unicode(time.strftime(obj, '%H:%M:%S.%f'))

        return obj


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
    fecha_emision = ndb.DateTimeProperty()
    fecha_recepcion = ndb.DateTimeProperty()
    estado_documento = ndb.StringProperty(choices=tipos_de_estados_documentos)
    tipo_operacion = ndb.StringProperty(choices=tipos_de_operaciones)
    tipo_receptor = ndb.StringProperty(choices=tipos_de_receptor)
    # campos correo
    nombre_cliente = ndb.StringProperty(required=False)
    correo = ndb.StringProperty(required=True)
    asunto = ndb.StringProperty(required=True)
    html = ndb.TextProperty(required=True)
    # adjuntos
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
    # campos click
    click_ip = ndb.StringProperty()
    click_purchase = ndb.StringProperty()
    click_useragent = ndb.StringProperty()
    click_event = ndb.StringProperty()
    click_email = ndb.StringProperty()
    click_date = ndb.DateTimeProperty()
    click_url = ndb.StringProperty()

    @classmethod
    def search_email(self, correo, numero_folio, tipo_dte):
        """ Retorna el objeto para determinar si existe o no """
        query = EmailModel.query()
        query = query.filter(EmailModel.correo == correo)
        query = query.filter(EmailModel.numero_folio == numero_folio)
        query = query.filter(EmailModel.tipo_dte == tipo_dte)
        return query.get()

    @ndb.transactional
    def email_add_count(self, data):
        """ Incrementa el campo de lecturas efectuadas 
            por el receptor del correo """
        data.opened_count = data.opened_count + 1
        data.put()

    @classmethod
    def get_info_by_email(self, date_from, date_to, correo):
        query = EmailModel.query()
        query = query.filter(EmailModel.correo == correo)
        query = query.filter(EmailModel.input_date >= date_from)
        query = query.filter(EmailModel.input_date <= date_to)
        query = query.order(-EmailModel.input_date)
        return query.fetch()

    @classmethod
    def get_emails_by_folio(self, folio):
        query = EmailModel.query()
        query = query.filter(EmailModel.numero_folio == folio)
        return query.fetch()

    @classmethod
    def get_email_lagging(self):
        query = EmailModel.query()
        query = query.filter(EmailModel.processed_event == None)
        query = query.filter(EmailModel.dropped_event == None)
        return query.fetch()

    @classmethod
    def get_emails_by_rut_receptor(self, date_from, date_to, rut):
        query = EmailModel.query()
        query = query.filter(EmailModel.input_date >= date_from)
        query = query.filter(EmailModel.input_date <= date_to)
        query = query.filter(EmailModel.rut_receptor == rut)
        query = query.order(-EmailModel.input_date)
        return query.fetch()

    @classmethod
    def get_stats_by_dates(self, from_date, to_date, tipo_receptor):
        # dias para restar
        day = timedelta(days=1)
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
            fecha = str(end_date).split(' ')[0]
            fecha = fecha.split('-')
            fecha.reverse()
            ''.join(fecha)
            fecha = fecha[0] + '-' + fecha[1]
            # Armar array de respuesta
            data = [
                fecha, total, processed, delivered, opened, dropped, bounced]
            data_result.append(data)
            end_date = end_date + day
        return data_result

    @classmethod
    def get_statistic_by_dates(self, from_date, to_date, tipo_receptor):
        query = EmailModel.query()
        if tipo_receptor == 'all':
            query = query.filter(EmailModel.input_date >= from_date)
            query = query.filter(EmailModel.input_date <= to_date)
        else:
            query = query.filter(EmailModel.input_date >= from_date)
            query = query.filter(EmailModel.input_date <= to_date)
            query = query.filter(EmailModel.tipo_receptor == tipo_receptor)
        total = query.count()
        processed = query.filter(EmailModel.processed_event == "processed").count()
        delivered = query.filter(EmailModel.delivered_event == "delivered").count()
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

    @classmethod
    def get_all_emails_by_dates(self, from_date, to_date, tipo_receptor):
        query = EmailModel.query()
        if tipo_receptor == 'all':
            query = query.filter(EmailModel.input_date >= from_date)
            query = query.filter(EmailModel.input_date <= to_date)
        else:
            query = query.filter(EmailModel.input_date >= from_date)
            query = query.filter(EmailModel.input_date <= to_date)
            query = query.filter(EmailModel.tipo_receptor == tipo_receptor)
        return query.fetch()

    @classmethod
    def get_all_sended_emails_by_dates(self, from_date, to_date, tipo_receptor):
        query = EmailModel.query()
        if tipo_receptor == 'all':
            query = query.filter(EmailModel.delivered_event == 'delivered')
            query = query.filter(EmailModel.input_date >= from_date)
            query = query.filter(EmailModel.input_date <= to_date)
        else:
            query = query.filter(EmailModel.delivered_event == 'delivered')
            query = query.filter(EmailModel.input_date >= from_date)
            query = query.filter(EmailModel.input_date <= to_date)
            query = query.filter(EmailModel.tipo_receptor == tipo_receptor)
        return query.fetch()

    @classmethod
    def get_all_failure_emails_by_dates(self, from_date, to_date, tipo_receptor='all'):
        query = EmailModel.query()
        if tipo_receptor == 'all':
            query = query.filter(ndb.OR(EmailModel.dropped_event == 'dropped', EmailModel.bounce_event == 'bounce'))
            query = query.filter(EmailModel.input_date >= from_date)
            query = query.filter(EmailModel.input_date <= to_date)
        else:
            query = query.filter(ndb.OR(EmailModel.dropped_event == 'dropped', EmailModel.bounce_event == 'bounce'))
            query = query.filter(EmailModel.input_date >= from_date)
            query = query.filter(EmailModel.input_date <= to_date)
            query = query.filter(EmailModel.tipo_receptor == tipo_receptor)
        return query.fetch()

    @classmethod
    def get_emails_by_mount(self, date_from, date_to, mount_from, mount_to, tipo_receptor='all'):
        query_from = EmailModel.query()
        query_from = query_from.filter(EmailModel.input_date >= date_from, EmailModel.input_date <= date_to)
        query_from_keys = query_from.fetch(None, keys_only=True)
        logging.info("paso query 1")
        logging.info(query_from.count())
        
        query_to = EmailModel.query()
        query_to = query_to.filter(EmailModel.monto >= mount_from, EmailModel.monto <= mount_to)
        query_to_keys = query_to.fetch(None, keys_only=True)
        logging.info("paso query 2")
        logging.info(query_to.count())

        valid_query_keys = list(set(query_from_keys) & set(query_to_keys))
        logging.info("largo query")
        logging.info(len(valid_query_keys))
        result = []
        if valid_query_keys:
            query = ndb.get_multi(valid_query_keys)
            logging.info(query)
            return query
        else:
            return []
