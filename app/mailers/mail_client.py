# encoding: utf-8
#!/usr/bin/env python


from sendgrid import SendGridClient
from sendgrid import Mail


class EmailClient(object):

    def create_mail(self, to, subject, html, attachments):
    	pass