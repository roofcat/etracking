# encoding: utf-8
#!/usr/bin/env python


from google.appengine.ext import ndb


class Email(ndb.Model):

    input_date = ndb.DateTimeProperty(auto_now_add=True)
    read_count = ndb.IntegerProperty(default=0)
    read_date = ndb.DateTimeProperty()
    campaign_id = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    subject = ndb.StringProperty(required=True)
    htmlBody = ndb.TextProperty(required=True)
    bounced = ndb.BooleanProperty(default=False)

    def search_email(self, email, campaign_id):
        return Email.query(ndb.AND(Email.email == email, Email.campaign_id == campaign_id)).get()

    def email_add_count(self, data):
        data.read_count = data.read_count + 1
        data.put()

    def set_as_bounced(self, data):
        data.bounced = True
        data.put()
