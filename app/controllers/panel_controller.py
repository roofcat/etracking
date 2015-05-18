# encoding: utf-8
#!/usr/bin/env python


import webapp2


from config.oauth2_utils import decorator
from config.oauth2_utils import user_info_service
from config.jinja_environment import JINJA_ENVIRONMENT


class HomePanelHandler(webapp2.RequestHandler):

	@decorator.oauth_required
	def get(self):
		try:
		    http = decorator.http()
		    data = user_info_service.userinfo().get().execute(http=http)
		    context = {
		        'data': data,
		    }
		    template = JINJA_ENVIRONMENT.get_template('panel/index.html')
		    self.response.write(template.render(context))
		except Exception:
			self.redirect('/')