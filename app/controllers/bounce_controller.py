# encoding: utf-8
#!/usr/bin/env python


import logging


from google.appengine.ext.webapp.mail_handlers import BounceNotification
from google.appengine.ext.webapp.mail_handlers import BounceNotificationHandler


class EmailClientBounceHandler(BounceNotificationHandler):

	def receive(self, bounce_notification):
		logging.info('Rebote recibido desde : %s' % bounce_notification.__dict__)