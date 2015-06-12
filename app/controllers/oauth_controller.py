# -*- coding: utf-8 -*-
#!/usr/bin/env python


import webapp2


from config.oauth2_utils import decorator
from config.oauth2_utils import revoke_access_token
from config.oauth2_utils import user_info_service
from config.jinja_environment import JINJA_ENVIRONMENT


class AuthHandler(webapp2.RequestHandler):

	@decorator.oauth_aware
	def get(self):
		if not decorator.has_credentials():
		    context = {
		        'url': decorator.authorize_url(),
		        'has_credentials': decorator.has_credentials(),
		    }
		    template = JINJA_ENVIRONMENT.get_template('auth.html')
		    self.response.write(template.render(context))
		else:
			self.redirect('/admin')


class RevokeHandler(webapp2.RequestHandler):

	@decorator.oauth_required
	def get(self):
		try:
		    token = decorator.credentials.access_token
		    revoke_access_token(token)
		finally:
		    self.redirect('/')