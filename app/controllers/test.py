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
