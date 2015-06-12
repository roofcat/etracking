# -*- coding: utf-8 -*-
#!/usr/bin/env python


import webapp2


from config.oauth2_utils import decorator
from config.oauth2_utils import user_info_service
from config.jinja_environment import JINJA_ENVIRONMENT


class HomePanelHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write("index")
