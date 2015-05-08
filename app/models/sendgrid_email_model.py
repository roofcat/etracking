# encoding: utf-8
#!/usr/bin/env python


from google.appengine.ext import ndb


class SendGridEmailModel(ndb.Model):
	"""
	email = 
	sg_event_id
	sg_message_id
	timestamp
	smtp-id
	event
	category
	id
	purchase
	uid
	"""