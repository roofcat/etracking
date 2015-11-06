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
    input_datetime = ndb.DateTimeProperty(auto_now_add=True, indexed=True)
    input_date = ndb.DateProperty(auto_now_add=True, indexed=True)
    # campos dte
    empresa = ndb.StringProperty(required=True, indexed=True)
    rut_receptor = ndb.StringProperty(required=True, indexed=True)
    rut_emisor = ndb.StringProperty(required=True, indexed=True)
    tipo_envio = ndb.StringProperty(required=True, choices=tipos_de_envio, indexed=True)
    tipo_dte = ndb.StringProperty(indexed=True)
    numero_folio = ndb.StringProperty(indexed=True)
    resolucion_receptor = ndb.StringProperty(indexed=True)
    resolucion_emisor = ndb.StringProperty(indexed=True)
    monto = ndb.IntegerProperty(indexed=True)
    fecha_emision = ndb.DateTimeProperty(indexed=True)
    fecha_recepcion = ndb.DateTimeProperty(indexed=True)
    estado_documento = ndb.StringProperty(choices=tipos_de_estados_documentos, indexed=True)
    tipo_operacion = ndb.StringProperty(choices=tipos_de_operaciones, indexed=True)
    tipo_receptor = ndb.StringProperty(choices=tipos_de_receptor, indexed=True)
    # campos correo
    nombre_cliente = ndb.StringProperty(required=False, indexed=True)
    correo = ndb.StringProperty(required=True, indexed=True)
    asunto = ndb.StringProperty(required=True)
    html = ndb.TextProperty(required=True)
    # adjuntos
    attachs = ndb.KeyProperty(kind='AttachModel', repeated=True)
    # campos de processed
    smtp_id = ndb.StringProperty(indexed=True)
    processed_date = ndb.DateTimeProperty(indexed=True)
    processed_event = ndb.StringProperty(indexed=True)
    processed_sg_event_id = ndb.StringProperty(indexed=True)
    processed_sg_message_id = ndb.StringProperty(indexed=True)
    # campos delivered
    delivered_date = ndb.DateTimeProperty(indexed=True)
    delivered_event = ndb.StringProperty(indexed=True)
    delivered_sg_event_id = ndb.StringProperty(indexed=True)
    delivered_sg_message_id = ndb.StringProperty(indexed=True)
    delivered_response = ndb.TextProperty()
    # campos open
    opened_first_date = ndb.DateTimeProperty(indexed=True)
    opened_last_date = ndb.DateTimeProperty(indexed=True)
    opened_event = ndb.StringProperty(indexed=True)
    opened_ip = ndb.StringProperty(indexed=True)
    opened_user_agent = ndb.StringProperty(indexed=True)
    opened_sg_event_id = ndb.StringProperty(indexed=True)
    opened_sg_message_id = ndb.StringProperty(indexed=True)
    opened_count = ndb.IntegerProperty(default=0, indexed=True)
    # campos dropped
    dropped_date = ndb.DateTimeProperty(indexed=True)
    dropped_sg_event_id = ndb.StringProperty(indexed=True)
    dropped_sg_message_id = ndb.StringProperty(indexed=True)
    dropped_reason = ndb.StringProperty(indexed=True)
    dropped_event = ndb.StringProperty(indexed=True)
    # campos bounce
    bounce_date = ndb.DateTimeProperty()
    bounce_event = ndb.StringProperty(indexed=True)
    bounce_sg_event_id = ndb.StringProperty(indexed=True)
    bounce_sg_message_id = ndb.StringProperty(indexed=True)
    bounce_reason = ndb.TextProperty()
    bounce_status = ndb.StringProperty(indexed=True)
    bounce_type = ndb.StringProperty(indexed=True)
    # campos unscribes
    unsubscribe_date = ndb.DateTimeProperty(indexed=True)
    unsubscribe_uid = ndb.StringProperty(indexed=True)
    unsubscribe_purchase = ndb.StringProperty(indexed=True)
    unsubscribe_id = ndb.StringProperty(indexed=True)
    unsubscribe_event = ndb.StringProperty(indexed=True)
    # campos click
    click_ip = ndb.StringProperty(indexed=True)
    click_purchase = ndb.StringProperty(indexed=True)
    click_useragent = ndb.StringProperty(indexed=True)
    click_event = ndb.StringProperty(indexed=True)
    click_email = ndb.StringProperty(indexed=True)
    click_date = ndb.DateTimeProperty(indexed=True)
    click_url = ndb.StringProperty(indexed=True)

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
        data.opened_count += 1
        data.put()

    @classmethod
    def get_info_by_email(self, date_from, date_to, correo, **opts):
        query = EmailModel.query()
        query = query.filter(EmailModel.correo == correo)
        query = query.filter(EmailModel.input_date >= date_from)
        query = query.filter(EmailModel.input_date <= date_to)
        query = query.order(-EmailModel.input_date)
        query_total = query.count()
        query = query.fetch(opts['display_length'], offset=opts['display_start'])
        if query:
            query_length = len(query)
        else:
            query_length = 0
        return {
            'query_total': query_total,
            'query_length': query_length,
            'data': query,
        }

    @classmethod
    def get_emails_by_folio(self, folio, **opts):
        query = EmailModel.query()
        query = query.filter(EmailModel.numero_folio == folio)
        query = query.order(-EmailModel.input_date)
        query_total = query.count()
        query = query.fetch(opts['display_length'], offset=opts['display_start'])
        if query:
            query_length = len(query)
        else:
            query_length = 0
        return {
            'query_total': query_total,
            'query_length': query_length,
            'data': query,
        }

    @classmethod
    def get_email_lagging(self):
        query = EmailModel.query()
        query = query.filter(EmailModel.processed_event == None)
        query = query.filter(EmailModel.dropped_event == None)
        return query.fetch()

    @classmethod
    def get_emails_by_rut_receptor(self, date_from, date_to, rut, **opts):
        query = EmailModel.query()
        query = query.filter(EmailModel.input_date >= date_from)
        query = query.filter(EmailModel.input_date <= date_to)
        query = query.filter(EmailModel.rut_receptor == rut)
        query = query.order(-EmailModel.input_date)
        query_total = query.count()
        query = query.fetch(opts['display_length'], offset=opts['display_start'])
        if query:
            query_length = len(query)
        else:
            query_length = 0
        return {
            'query_total': query_total,
            'query_length': query_length,
            'data': query,
        }

    @classmethod
    def get_stats_by_dates(self, date_from, date_to, tipo_receptor):
        # dias para restar
        day = timedelta(days=1)
        end_date = date_from
        # arreglo para armar el objeto de respuesta
        data_result = [
            ["Fecha", "Solicitudes", "Procesados", "Enviados",
                "Abiertos", "Rechazados", "Rebotados"]
        ]
        while end_date <= date_to:
            if tipo_receptor == 'all':
                query = EmailModel.query(EmailModel.input_date == end_date)
            else:
                query = EmailModel.query(EmailModel.input_date == end_date,
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
    def get_statistic_by_dates(self, date_from, date_to, tipo_receptor):
        query = EmailModel.query()
        if tipo_receptor == 'all':
            query = query.filter(EmailModel.input_date >= date_from)
            query = query.filter(EmailModel.input_date <= date_to)
        else:
            query = query.filter(EmailModel.input_date >= date_from)
            query = query.filter(EmailModel.input_date <= date_to)
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
    def get_all_emails_by_dates(self, date_from, date_to, tipo_receptor='all'):
        query = EmailModel.query()
        query = query.filter(EmailModel.input_date >= date_from)
        query = query.filter(EmailModel.input_date <= date_to)
        if tipo_receptor != 'all':
            query = query.filter(EmailModel.tipo_receptor == tipo_receptor)
        query = query.order(-EmailModel.input_date)
        return query.fetch()

    @classmethod
    def get_all_emails_by_dates_async(self, date_from, date_to, tipo_receptor='all'):
        query = EmailModel.query()
        query = query.filter(EmailModel.input_date >= date_from)
        query = query.filter(EmailModel.input_date <= date_to)
        if tipo_receptor != 'all':
            query = query.filter(EmailModel.tipo_receptor == tipo_receptor)
        query = query.order(-EmailModel.input_date)
        future = query.fetch_async(limit=None, batch_size=500)
        return future

    @classmethod
    def get_all_sended_emails_by_dates(self, date_from, date_to, tipo_receptor='all'):
        query = EmailModel.query()
        if tipo_receptor == 'all':
            query = query.filter(EmailModel.delivered_event == 'delivered')
            query = query.filter(EmailModel.input_date >= date_from)
            query = query.filter(EmailModel.input_date <= date_to)
        else:
            query = query.filter(EmailModel.delivered_event == 'delivered')
            query = query.filter(EmailModel.input_date >= date_from)
            query = query.filter(EmailModel.input_date <= date_to)
            query = query.filter(EmailModel.tipo_receptor == tipo_receptor)
        return query.fetch()

    @classmethod
    def get_all_failure_emails_by_dates(self, date_from, date_to, tipo_receptor='all', **opts):
        query = EmailModel.query()
        if tipo_receptor == 'all':
            query = query.filter(ndb.OR(EmailModel.dropped_event == 'dropped', EmailModel.bounce_event == 'bounce'))
            query = query.filter(EmailModel.input_date >= date_from)
            query = query.filter(EmailModel.input_date <= date_to)
        else:
            query = query.filter(ndb.OR(EmailModel.dropped_event == 'dropped', EmailModel.bounce_event == 'bounce'))
            query = query.filter(EmailModel.input_date >= date_from)
            query = query.filter(EmailModel.input_date <= date_to)
            query = query.filter(EmailModel.tipo_receptor == tipo_receptor)
        query = query.order(-EmailModel.input_date)
        query_total = query.count()
        query = query.fetch(opts['display_length'], offset=opts['display_start'])
        if query:
            query_length = len(query)
        else:
            query_length = 0
        return {
            'query_total': query_total,
            'query_length': query_length,
            'data': query,
        }

    @classmethod
    def get_emails_by_mount(self, date_from, date_to, mount_from, mount_to, tipo_receptor='all', **opts):
        query_from = EmailModel.query()
        query_from = query_from.filter(EmailModel.input_date >= date_from, EmailModel.input_date <= date_to)
        query_from_keys = query_from.fetch(None, keys_only=True)
        
        query_to = EmailModel.query()
        query_to = query_to.filter(EmailModel.monto >= mount_from, EmailModel.monto <= mount_to)
        query_to_keys = query_to.fetch(None, keys_only=True)

        # se procede con la union de 2 listas
        valid_query_keys = list(set(query_from_keys) & set(query_to_keys))

        if valid_query_keys:
            query = ndb.get_multi(valid_query_keys)
            query_total = len(query)
            # filtrado del array completo con un desde hasta
            array_from = opts['display_start']
            array_to = opts['display_length']
            if array_from == 0:
                query = query[array_from:array_to]
            else:
                query = query[array_from:array_from + array_to]
            query_length = len(query)
            return {
                'query_total': query_total,
                'query_length': query_length,
                'data': query
            }
        else:
            return {
                'query_total': 0,
                'query_length': 0,
                'data': []
            }
