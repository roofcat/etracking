# encoding:utf-8
#!/usr/bin/env python


from google.appengine.api import mail


class EmailClient(object):

    def create_mail(self, to, subject, htmlBody, attachments):

        mail.send_mail(
            sender='crojas@azurian.com',
            to=to,
            subject=subject,
            body='',
            html=htmlBody,
            attachments=attachments
        )
