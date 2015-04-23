# encoding: utf-8
#!/usr/bin/env python


import webapp2
import urllib2


from google.appengine.api.mail import Attachment


from app.models.email_model import Email
from app.mailers.mail_client import EmailClient


class InputEmailHandler(webapp2.RequestHandler):

    def post(self):
        campaign_id = self.request.get('campaign_id')
        email = self.request.get('email')
        subject = self.request.get('subject')
        htmlBody = self.request.get('htmlBody')

        url = 'http://azurian-rastreo.appspot.com/track?email=' + email + '&campaign_id=' + campaign_id
        htmlBody = htmlBody + '<div><img src="' + urllib2.url2pathname(url) + '" width="1" height="1" border="0" /></div>'
        
        attach = self.request.POST.get('attach', None)
        attachments = [Attachment(attach.filename, attach.file.read())]
        
        if (campaign_id and email and subject and htmlBody):
            o_mail = Email()
            result = o_mail.search_email(email, campaign_id)
            if not result:
                o_mail.campaign_id = campaign_id
                o_mail.email = email
                o_mail.subject = subject
                o_mail.htmlBody = htmlBody
                o_mail.put()
            new_mail = EmailClient()
            new_mail.create_mail(
                to=email,
                subject=subject,
                html=htmlBody,
                attachments=attachments
            )
        else:
            self.response.write('Error')
