# encoding: utf-8
#!/usr/bin/env python


import webapp2


from app.models.email_model import Email


class EmailTrackHandler(webapp2.RequestHandler):

	def get(self):
		email = self.request.get('email')
		campaign_id = self.request.get('campaign_id')

		o_email = Email()
		result = o_email.search_email(email, campaign_id)
		if result:
			o_email.email_add_count(result)
		else:
			self.response.write('Datos no existentes')