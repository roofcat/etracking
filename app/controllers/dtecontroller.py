# encoding: utf-8
#!/usr/bin/env python


import webapp2
import urllib2


from google.appengine.api.mail import Attachment


from app.models.email_model import Email
from app.mailers.mail_client import EmailClient


class Formulario(webapp2.RequestHandler):

    def get(self):
        form = """
		<form method="POST" enctype="multipart/form-data">
		    <input type="text" name="campaign_id"><br>
		    <input type="email" name="email"><br>
		    <input type="text" name="subject"><br>
		    <textarea name="htmlBody" id="" cols="30" rows="10"></textarea>
		  	<input type="file" name="attach"><br>
		  	<input type="submit"name="submit" value="Enviar">
		</form>"""
        self.response.write(form)

    def post(self):
        campaign_id = self.request.get('campaign_id')
        email = self.request.get('email')
        subject = self.request.get('subject')
        htmlBody = self.request.get('htmlBody')
        #attach = self.request.POST.get('attach', None)
        attach = self.request.get_all('attach')
        self.response.write(self.request.body)
        myfiles = []
        for att in attach:
                # myfiles.append(att)
            self.response.write(att)
"""
    def post(self):
        campaign_id = self.request.get('campaign_id')
        email = self.request.get('email')
        subject = self.request.get('subject')
        htmlBody = self.request.get('htmlBody')
        attach = self.request.POST.get('attach', None)
        att = Attachment(attach.filename, attach.file.read())
        new_mail = EmailClient()
        new_mail.create_mail(
            to=email,
            subject=subject,
            html=htmlBody,
            attachments=att
        )
"""


class InputEmailHandler(webapp2.RequestHandler):

    def post(self):
        campaign_id = self.request.get('campaign_id')
        email = self.request.get('email')
        subject = self.request.get('subject')
        htmlBody = self.request.get('htmlBody')
        url = 'http://azurian-rastreo.appspot.com/track?email=' + \
            email + '&campaign_id=' + campaign_id
        htmlBody = htmlBody + '<div><img src="' + \
            urllib2.url2pathname(
                url) + '" width="1" height="1" border="0" /></div>'
        attach = self.request.POST.get('attach', None)
        attachments = [Attachment(attach.filename, attach.file.read())]
        #attachments.append(Attachment(attach.filename, attach.file.read()))
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
