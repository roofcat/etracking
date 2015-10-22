# -*- coding: utf-8 -*-
#!/usr/bin/env python


import webapp2
import json
import logging
import base64
import re
import datetime
import mimetypes
import tablib
import StringIO


from google.appengine.ext import ndb


from app.models.email import EmailModel
from app.models.email import AttachModel
from app.models.email import JSONEncoder
from config.jinja_environment import JINJA_ENVIRONMENT


class TabLibHandler(webapp2.RequestHandler):

    def get(self):
        from_date = 1444791600
        to_date = 1445396400
        from_date = int(from_date)
        date_to = int(to_date)
        from_date = datetime.datetime.fromtimestamp(from_date)
        to_date = datetime.datetime.fromtimestamp(to_date)
        data = EmailModel.get_all_sended_emails_by_dates(from_date, to_date, 'all')
        my_tab = tablib.Dataset()
        my_tab.headers = (
            'datetime', 'empresa', 'rut_receptor', 'rut_emisor', 'tipo_envio', 'tipo_dte', 
            'numero_folio', 'resolucion_receptor', 'resolucion_emisor', 'monto', 
            'fecha_emision', 'fecha_recepcion', 'estado_documento', 'tipo_operacion', 
            'tipo_receptor', 'nombre_cliente', 'correo', 'asunto', 'fecha_procesado', 
            'procesado', 'fecha_envio', 'enviado', 'respuesta_envio', 'fecha_primera_lectura', 
            'fecha_ultima_lectura', 'abierto', 'ip_lector', 'navegador_lectura', 
            'cantidad_lectura', 'fecha_drop', 'razon_drop', 'drop', 'fecha_rebote', 
            'rebote', 'motivo_rebote', 'estado_Rebote', 'tipo_rebote', 'fecha_unsubscribe', 
            'unsubscribe_purchase', 'unsubscribe_id', 'unsubscribe', 'click_ip', 'click_purchase', 
            'click_navegador', 'click_event', 'click_email', 'fecha_click', 'click_url'
        )
        for row in data:
            #logging.info(row)
            input_datetime = str(row.input_datetime)
            if row.empresa:
                empresa = unicode(row.empresa).encode('utf-8')
            else:
                empresa = ''
            if row.rut_receptor:
                rut_receptor = row.rut_receptor
            else:
                rut_receptor = ''
            if row.rut_emisor:
                rut_emisor = row.rut_emisor
            else:
                rut_emisor = ''
            if row.tipo_envio:
                tipo_envio = row.tipo_envio
            else:
                tipo_envio = ''
            if row.tipo_dte:
                tipo_dte = row.tipo_dte
            else:
                tipo_dte = ''
            if row.numero_folio:
                numero_folio = row.numero_folio
            else:
                numero_folio = ''
            if row.resolucion_receptor:
                resolucion_receptor = row.resolucion_receptor
            else:
                resolucion_receptor = ''
            if row.resolucion_emisor:
                resolucion_emisor = row.resolucion_emisor
            else:
                resolucion_emisor = ''
            if row.monto:
                monto = row.monto
            else:
                monto = 0
            if row.fecha_emision:
                fecha_emision = row.fecha_emision
            else:
                fecha_emision = ''
            if row.fecha_recepcion:
                fecha_recepcion = row.fecha_recepcion
            else:
                fecha_recepcion = ''
            if row.estado_documento:
                estado_documento = row.estado_documento
            else:
                estado_documento = ''
            if row.tipo_operacion:
                tipo_operacion = row.tipo_operacion
            else:
                tipo_operacion = ''
            if row.tipo_receptor:
                tipo_receptor = row.tipo_receptor
            else:
                tipo_receptor = ''
            if row.nombre_cliente:
                nombre_cliente = row.nombre_cliente
            else:
                nombre_cliente = ''
            if row.correo:
                correo = row.correo
            else:
                correo = ''
            if row.asunto:
                asunto = row.asunto
            else:
                asunto = ''
            processed_date = row.processed_date
            processed_event = row.processed_event
            delivered_date = row.delivered_date
            delivered_event = row.delivered_event
            delivered_response = row.delivered_response
            opened_first_date = row.opened_first_date
            opened_last_date = row.opened_last_date
            opened_event = row.opened_event
            opened_ip = row.opened_ip
            if row.opened_user_agent:
                opened_user_agent = row.opened_user_agent
            else:
                opened_user_agent = ''
            opened_count = row.opened_count
            dropped_date = row.dropped_date
            if row.dropped_reason:
                dropped_reason = row.dropped_reason
            else:
                dropped_reason = ''
            dropped_event = row.dropped_event
            bounce_date = row.bounce_date
            bounce_event = row.bounce_event
            if row.bounce_reason:
                bounce_reason = row.bounce_reason
            else:
                bounce_reason = ''
            bounce_status = row.bounce_status
            bounce_type = row.bounce_type
            unsubscribe_date = row.unsubscribe_date
            unsubscribe_purchase = row.unsubscribe_purchase
            unsubscribe_id = row.unsubscribe_id
            unsubscribe_event = row.unsubscribe_event
            click_ip = row.click_ip
            click_purchase = row.click_purchase
            if row.click_useragent:
                click_useragent = row.click_useragent
            else:
                click_useragent = ''
            click_event = row.click_event
            click_email = row.click_email
            click_date = row.click_date
            click_url = row.click_url
            csv_row = (
                input_datetime, empresa, rut_receptor, rut_emisor, tipo_envio, tipo_dte, 
                numero_folio, resolucion_receptor, resolucion_emisor, monto, fecha_emision, 
                fecha_recepcion, estado_documento, tipo_operacion, tipo_receptor, 
                nombre_cliente, correo, asunto, processed_date, processed_event, 
                delivered_date, delivered_event, delivered_response, opened_first_date, 
                opened_last_date, opened_event, opened_ip, opened_user_agent, opened_count, 
                dropped_date, dropped_reason, dropped_event, bounce_date, bounce_event, 
                bounce_reason, bounce_status, bounce_type, unsubscribe_date, 
                unsubscribe_purchase, unsubscribe_id, unsubscribe_event, click_ip, click_purchase, 
                click_useragent, click_event, click_email, click_date, click_url
            )
            my_tab.append(csv_row)
        self.response.headers['Content-Type'] = 'application/xlsx'
        self.response.headers['Content-Disposition'] = 'attachment; filename=my_excel.xlsx'
        self.response.write(my_tab.xlsx)


class QueriesHandler(webapp2.RequestHandler):

    def get(self):
        query_opts = {}
        query_opts['batch_size'] = 500
        from_date = 1443668400
        to_date = 1444964400
        from_date = int(from_date)
        date_to = int(to_date)
        from_date = datetime.datetime.fromtimestamp(from_date)
        to_date = datetime.datetime.fromtimestamp(to_date)
        query = EmailModel.query()
        query = query.filter(ndb.OR(EmailModel.dropped_event == 'dropped', EmailModel.bounce_event == 'bounce'))
        query = query.filter(EmailModel.input_date >= from_date)
        query = query.filter(EmailModel.input_date <= to_date)
        query = query.fetch_async(limit=None, **query_opts)
        logging.info(query)
        for q in query:
            self.response.write(q)


class TestViewFileHandler(webapp2.RequestHandler):

    def get(self, file_id):
        if file_id:
            logging.info(file_id)
            file_id = str(file_id)
            attach = ndb.Key(urlsafe=file_id).get()
            logging.info(attach.nombre)
            logging.info(attach.archivo)
            logging.info(mimetypes.guess_type(attach.nombre)[0])
            self.response.headers['Content-Type'] = mimetypes.guess_type(attach.nombre)[0]
            self.response.write(attach.archivo)
        else:
            self.response.write("nada")



class TestHandler(webapp2.RequestHandler):

    def get(self):
        date_from = 1444618800
        date_to = 1445223600
        date_from = datetime.datetime.fromtimestamp(date_from)
        date_to = datetime.datetime.fromtimestamp(date_to)
        query = EmailModel.query()
        query = query.filter(EmailModel.input_date >= date_from)
        query = query.filter(EmailModel.input_date <= date_to)
        processed = query.filter(EmailModel.processed_event == "processed")
        delivered = query.filter(EmailModel.delivered_event == "delivered")
        opened = query.filter(EmailModel.opened_event == "open")
        dropped = query.filter(EmailModel.dropped_event == "dropped")
        bounced = query.filter(EmailModel.bounce_event == "bounce")
        context = {
            'processed': processed,
            'delivered': delivered,
            'opened': opened,
            'dropped': dropped,
            'bounced': bounced,
        }
        #self.response.write(json.dumps(context))
        self.response.write(processed.__dict__)


class Test0Handler(webapp2.RequestHandler):

    def get(self):
        total_count = EmailModel.query().count()
        total_processed = EmailModel.query(EmailModel.processed_event == 'processed').count()
        total_delivered = EmailModel.query(EmailModel.delivered_event == 'delivered').count()
        total_opened = EmailModel.query(EmailModel.opened_event == 'open').count()
        total_dropped = EmailModel.query(EmailModel.dropped_event == 'dropped').count()
        total_bounce = EmailModel.query(EmailModel.bounce_event == 'bounce').count()
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
        date_from = 1441854000
        date_to = 1442458800
        date_from = datetime.datetime.fromtimestamp(date_from)
        date_to = datetime.datetime.fromtimestamp(date_to)
        query = EmailModel.get_info_by_email(date_from, date_to, 'admin@gapps.azurian.com')
        result = []
        for q in query:
            result.append(JSONEncoder().default(q))
        #self.response.write(JSONEncoder().default(query))
        self.response.headers['Content-Type'] = 'text/json'
        self.response.write(json.dumps(result))


class Test3Handler(webapp2.RequestHandler):

    def get(self):
        date_from = '1442804400'
        date_to = '1443409200'
        mount_from = '0'
        mount_to = '0'
        date_from = int(date_from, base=10)
        date_to = int(date_to, base=10)
        mount_from = int(mount_from, base=10)
        mount_to = int(mount_to, base=10)
        date_from = datetime.datetime.fromtimestamp(date_from)
        date_to = datetime.datetime.fromtimestamp(date_to)
        query = EmailModel.get_emails_by_mount(date_from, date_to, mount_from, mount_to)
        result = []
        for q in query:
            result.append(JSONEncoder().default(q))
        #self.response.write(JSONEncoder().default(query))
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(result)


class Test4Handler(webapp2.RequestHandler):

    def get(self):
        """
        todo = EmailModel.query(group_by=['input_date'], projection=['input_date'], distinct=True).count()
        self.response.write(json.dumps(todo))
        """
        consulta = EmailModel.query(EmailModel.correo == "fromero@aliter.cl").get()
        consulta.bounce_reason = "550 No existe ese usuario en esta direccion"
        consulta.put()


class Test5Handler(webapp2.RequestHandler):
    
    def get(self):
        todo = EmailModel.query().fetch()
        output = StringIO.StringIO()
        csv_out = csv.writer(output)

        csv_out.writerow(["datetime", "date", "documento", "md5", "correo", "fecha_procesado", "procesado",
            "fecha_envio", "enviado", "fecha_lectura", "leido", "ip", "fecha_rechazo", "razon_rechazo",
            "rechazado", "fecha_rebote", "rebotado", "razon_rebote", "estado_rebote", "tipo_rebote",])
        for row in todo:
            input_datetime = str(row.input_datetime)
            input_date = str(row.input_date)
            if not row.tipo_dte == None:
                tipo_dte = str(row.tipo_dte)
            else:
                tipo_dte = ""
            if not row.numero_folio == None:
                numero_folio = str(row.numero_folio)
            else:
                numero_folio = ""
            if not row.correo == None:
                correo = str(row.correo)
                logging.info(correo)
            else:
                correo = ""
            if not row.processed_date == None:
                processed_date = str(row.processed_date)
            else:
                processed_date = ""
            if not row.processed_event == None:
                processed_event = str(row.processed_event)
            else:
                processed_event = ""
            if not row.delivered_date == None:
                delivered_date = str(row.delivered_date)
            else:
                delivered_date = ""
            if not row.delivered_event == None:
                delivered_event = str(row.delivered_event)
            else:
                delivered_event = ""
            if not row.opened_first_date == None:
                opened_first_date = str(row.opened_first_date)
            else:
                opened_first_date = ""
            if not row.opened_event == None:
                opened_event = str(row.opened_event)
            else:
                opened_event = ""
            if not row.opened_ip == None:
                opened_ip = str(row.opened_ip)
            else:
                opened_ip = ""
            if not row.dropped_date == None:
                dropped_date = str(row.dropped_date)
            else:
                dropped_date = ""
            if not row.dropped_reason == None:
                dropped_reason = str(row.dropped_reason)
            else:
                dropped_reason = ""
            if not row.dropped_event == None:
                dropped_event = str(row.dropped_event)
            else:
                dropped_event = ""
            if not row.bounce_date == None:
                bounce_date = str(row.bounce_date)
            else:
                bounce_date = ""
            if not row.bounce_event == None:
                bounce_event = str(row.bounce_event)
            else:
                bounce_event = ""
            if not row.bounce_reason == None:
                logging.info(row.bounce_reason)
                bounce_reason = " ".join(str(row.bounce_reason).splitlines())
                logging.info(bounce_reason)
            else:
                bounce_reason = ""
            if not row.bounce_status == None:
                bounce_status = str(row.bounce_status)
            else:
                bounce_status = ""
            if not row.bounce_type == None:
                bounce_type = str(row.bounce_type)
            else:
                bounce_type = ""
            csv_out.writerow([input_datetime, input_date, tipo_dte, numero_folio, correo, 
                processed_date, processed_event, delivered_date, delivered_event, 
                opened_first_date, opened_event, opened_ip, dropped_date, dropped_reason, 
                dropped_event, bounce_date, bounce_event, bounce_reason, bounce_status, 
                bounce_type])
        self.response.headers['Content-Type'] = 'text/csv'
        self.response.headers['Content-Disposition'] = 'attachment; filename=file.csv'
        content = output.getvalue()
        output.close()
        self.response.out.write(content)


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
