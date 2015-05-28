# encoding: utf-8
#!/usr/bin/env python


import webapp2
import json


from app.models.email_model import EmailModel


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
