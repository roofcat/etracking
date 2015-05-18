# encoding: utf-8
#!/usr/bin/env python


import webapp2


from app.models.email_model import EmailModel


class TestHandler(webapp2.RequestHandler):

	def get(self):

		e = EmailModel()
		results = e.get_all_emails()
		for r in results:
			self.response.write(r)
			self.response.write('<br>======')