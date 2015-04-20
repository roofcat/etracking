# encoding: utf-8
#!/usr/bin/env python


import webapp2
import urllib2


from google.appengine.api import mail


from app.models.email_model import Email
from app.mailers.email import MailingTool


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
        attach = self.request.POST.get('attach', None)
        att = mail.Attachment(attach.filename, attach.file.read())
        # self.response.write(attach.file.read())
        mail.send_mail(
            sender='crojas@azurian.com',
            to=email,
            subject=subject,
            body='',
            html=htmlBody,
            attachments=att
        )


class InputEmailHandler(webapp2.RequestHandler):

    def post(self):
        campaign_id = self.request.get('campaign_id')
        email = self.request.get('email')
        subject = self.request.get('subject')
        htmlBody = self.request.get('htmlBody')
        url = 'http://azurian-rastreo.appspot.com/track?email=' + email + '&campaign_id=' + campaign_id
        htmlBody = htmlBody + '<div><img src="' + urllib2.url2pathname(url) + '" width="1" height="1" border="0" /></div>'
        attach = self.request.POST.getall('attach')
        files = []
        for att in attach:
            files.append(mail.Attachment(att.filename, att.file.read()))
        
        if (campaign_id and email and subject and htmlBody):
            o_mail = Email()
            o_mail.campaign_id = campaign_id
            o_mail.email = email
            o_mail.subject = subject
            o_mail.htmlBody = htmlBody
            o_mail.put()
            mail.send_mail(
                sender='crojas@azurian.com',
                to=o_mail.email,
                subject=o_mail.subject,
                body='',
                html=o_mail.htmlBody,
                attachments=files
            )
        else:
            self.response.write('Error')
