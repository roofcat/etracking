# -*- coding: utf-8 -*-
#!/usr/bin/env python


from google.appengine.ext import ndb


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
        """ Incrementa el campo de lecturas efectuadas por el receptor del correo
        """
        data.opened_count = data.opened_count + 1
        data.put()

    @classmethod
    def get_count_statistic_by_dates(self, from_date, to_date):
        try:
            total = len(EmailModel.query(
                        ndb.AND(EmailModel.input_date >= from_date, 
                                EmailModel.input_date <= to_date)).fetch())
            processed = len(EmailModel.query(
                        ndb.AND(EmailModel.processed_event == 'processed',
                                EmailModel.input_date >= from_date, 
                                EmailModel.input_date <= to_date)).fetch())
            delivered = len(EmailModel.query(
                        ndb.AND(EmailModel.delivered_event == 'delivered',
                                EmailModel.input_date >= from_date, 
                                EmailModel.input_date <= to_date)).fetch())
            opened = len(EmailModel.query(
                        ndb.AND(EmailModel.opened_event == 'open',
                                EmailModel.input_date >= from_date,
                                EmailModel.input_date <= to_date)).fetch())
            dropped = len(EmailModel.query(
                        ndb.AND(EmailModel.dropped_event == 'dropped',
                                EmailModel.input_date >= from_date,
                                EmailModel.input_date <= to_date)).fetch())
            bounced = len(EmailModel.query(
                        ndb.AND(EmailModel.bounce_event == 'bounce',
                                EmailModel.input_date >= from_date,
                                EmailModel.input_date <= to_date)).fetch())
            return {
                'total': total,
                'processed': processed,
                'delivered': delivered,
                'opened': opened,
                'dropped': dropped,
                'bounced': bounced,
            }
            #return ndb.gql("SELECT * FROM EmailModel WHERE processed_event = 'processed' AND input_date >= :1 AND input_date <= :2", from_date, to_date).fetch()
        except Exception, e:
            raise e