# encoding: utf-8
#!/usr/bin/env python


import logging


from google.appengine.ext.webapp.mail_handlers import BounceNotification
from google.appengine.ext.webapp.mail_handlers import BounceNotificationHandler


class EmailClientBounceHandler(BounceNotificationHandler):

	def receive(self, bounce_message):
		logging.info('Rebote recibido post : %s' % str(self.request))
		logging.info('Rebote original : %s' % bounce_message.original)
		logging.info('Rebote notification : %s' % bounce_message.notification)
		logging.info('Rebote diccionario : %s' % bounce_message.__dict__)