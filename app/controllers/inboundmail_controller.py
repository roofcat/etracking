# encoding: utf-8
#!/usr/bin/env python


import logging


from google.appengine.ext.webapp.mail_handlers import InboundMailHandler


class EmailClientInboundHandler(InboundMailHandler):

	def receive(self, mail_message):
		logging.info("Mensaje recibido : " + mail_message.original)