# -*- coding: utf-8 -*-
#!/usr/bin/env python


import datetime


from google.appengine.ext import ndb


recipient_type_choices = ['dte', 'cliente', ]
options = ['all', 'dte', 'customer',]


class AttachModel(ndb.Model):
    name = ndb.StringProperty()
    attach = ndb.BlobProperty()


class EmailModel(ndb.Model):
    # campos basicos
    input_datetime = ndb.DateTimeProperty(auto_now_add=True)
    input_date = ndb.DateProperty(auto_now_add=True)
    input_time = ndb.TimeProperty(auto_now_add=True)
    enterprise = ndb.StringProperty(required=True)
    campaign_id = ndb.StringProperty(required=True)
    recipient_type = ndb.StringProperty(
        required=True, choices=recipient_type_choices)
    email = ndb.StringProperty(required=True)
    full_name = ndb.StringProperty(required=False)
    subject = ndb.StringProperty(required=True)
    htmlBody = ndb.TextProperty(required=True)
    # adjuntos
    #attachs = ndb.StructuredProperty(AttachModel, repeated=True)
    attachs = ndb.KeyProperty(kind='AttachModel', repeated=True)
    # capos de processed
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

    def search_email(self, enterprise, email, campaign_id):
        """ Retorna el objeto deseado en base a id campaña y el email
        para su posterior manipulación.
        """
        return EmailModel.query(ndb.AND(
            EmailModel.enterprise == enterprise,
            EmailModel.email == email,
            EmailModel.campaign_id == campaign_id
        )).get()

    def email_add_count(self, data):
        """ Incrementa el campo de lecturas efectuadas 
            por el receptor del correo
        """
        data.opened_count = data.opened_count + 1
        data.put()

    @classmethod
    def get_stats_by_dates(self, from_date, to_date, enterprise, options):
        # dias para restar
        day = datetime.timedelta(days=1)
        end_date = from_date
        data_result = [
            ["Fecha", "Solicitudes", "Procesados", "Enviados", "Abiertos", "Rechazados", "Rebotados"]
        ]
        
        while end_date <= to_date:
            query = EmailModel.query(EmailModel.input_date >= end_date,
                                    EmailModel.input_date <= end_date,
                                    EmailModel.enterprise == enterprise)
            total = query.count()
            processed = query.filter(EmailModel.processed_event == "processed").count()
            delivered = query.filter(EmailModel.delivered_event == "delivered").count()
            opened = query.filter(EmailModel.opened_event == "open").count()
            dropped = query.filter(EmailModel.dropped_event == "dropped").count()
            bounced = query.filter(EmailModel.bounce_event == "bounce").count()
            data = [str(end_date), total, processed, delivered, opened, dropped, bounced]
            data_result.append(data)
            end_date = end_date + day
        return data_result


    @classmethod
    def get_statistic_by_dates(self, from_date, to_date, enterprise, options):
        query = EmailModel.query(EmailModel.input_date >= from_date,
                                EmailModel.input_date <= to_date,
                                EmailModel.enterprise == enterprise)
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
