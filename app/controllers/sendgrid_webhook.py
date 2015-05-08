# encoding: utf-8
#!/usr/bin/env python


import logging
import webapp2
import json


class SendrigWebhookHandler(webapp2.RequestHandler):

	def post(self):
		bodyEvent = json.loads(self.request.body)
		for body in bodyEvent:
			email = body['email'] if body['email'] else ''
			try:
				ip = body['ip']
			except:
				ip = ''
			sg_event_id = body['sg_event_id'] if body['sg_event_id'] else ''
			sg_message_id = body['sg_message_id'] if body['sg_message_id'] else ''
			event = body['event'] if body['event'] else ''
			timestamp = body['timestamp'] if body['timestamp'] else ''
			try:
				useragent = body['useragent']
			except:
				useragent = ''
			try:
				response = body['response']
			except:
				response = body['response']
			try:
				smtp_id = body['smtp_id']
			except:
				smtp_id = ''
			logging.info(email)
			logging.info(event)
			logging.info(ip)
			logging.info(timestamp)
		logging.info(bodyEvent)