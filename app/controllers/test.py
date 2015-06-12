# encoding: utf-8
#!/usr/bin/env python


import webapp2
import json
import logging
import base64
import re


from app.models.email import EmailModel


class TestHandler(webapp2.RequestHandler):

	def get(self):
		total_count = len(EmailModel.query().fetch())
		total_processed = len(EmailModel.query(EmailModel.procesed_event == 'processed').fetch())
		total_delivered = len(EmailModel.query(EmailModel.delivered_event == 'delivered').fetch())
		total_opened = len(EmailModel.query(EmailModel.opened_event == 'open').fetch())
		total_dropped = len(EmailModel.query(EmailModel.dropped_event == 'dropped').fetch())
		total_bounce = len(EmailModel.query(EmailModel.bounce_event == 'bounce').fetch())
		context = {
			'total_count': total_count,
			'total_processed': total_processed,
			'total_delivered': total_delivered,
			'total_opened': total_opened,
			'total_dropped': total_dropped,
			'total_bounce': total_bounce,
		}
		self.response.write(json.dumps(context))


class TestInputWithUserAndPassword(webapp2.RequestHandler):

	def get(self):
		logging.info(self.request.headers)
		logging.info(self.request.body)
		headers = self.request.headers
		auth = headers['Authorization']
		logging.info(auth)
		auth = re.sub('^Basic ', '', auth)
		user, password = base64.decodestring(auth).split(':')
		logging.info(user)
		logging.info(password)
