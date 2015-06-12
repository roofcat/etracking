# -*- coding: utf-8 -*-
#!/usr/bin/env python


import webapp2


from config.oauth2_utils import decorator
from config.oauth2_utils import user_info_service
from config.jinja_environment import JINJA_ENVIRONMENT


class AdminHandler(webapp2.RequestHandler):
	@decorator.oauth_required
	def get(self):
		http = decorator.http()
		data = user_info_service.userinfo().get().execute(http=http)
		template = JINJA_ENVIRONMENT.get_template('admin/index.html')
		context = {
			'data': data,
		}
		self.response.write(template.render(context))
