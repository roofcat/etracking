# encoding: utf-8
#!/usr/bin/env python


import webapp2
import urllib2


from app.models.email_model import Email
from app.mailers.mail_client import EmailClient


class InputEmailHandler(webapp2.RequestHandler):

    def post(self):
        campaign_id = self.request.get('campaign_id')
        email = self.request.get('email')
        subject = self.request.get('subject')
        htmlBody = self.request.get('htmlBody')
        
        #attach = self.request.POST.get('attach', None)
        #attachments = [Attachment(attach.filename, attach.file.read())]
        
        if (campaign_id and email and subject and htmlBody):
            pass
        else:
            self.response.write('Error')
