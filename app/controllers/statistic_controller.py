# -*- coding: utf-8 -*-
#!/usr/bin/env python


import webapp2
import json
import logging
import datetime


from config.oauth2_utils import decorator
from config.oauth2_utils import user_info_service
from config.jinja_environment import JINJA_ENVIRONMENT


from app.models.email import EmailModel


class IndexStatisticHandler(webapp2.RequestHandler):
	@decorator.oauth_required
	def get(self):
		http = decorator.http()
		data = user_info_service.userinfo().get().execute(http=http)
		context = {
			'data': data,
		}
		template = JINJA_ENVIRONMENT.get_template('statistic/index.html')
		self.response.write(template.render(context))


class GraphStatisticHandler(webapp2.RequestHandler):
	@decorator.oauth_required
	def get(self):
		http = decorator.http()
		param_from = int(self.request.get('from_date'))
		param_to = int(self.request.get('to_date'))
		logging.info(param_from)
		logging.info(param_to)
		param_from = datetime.datetime.fromtimestamp(param_from)
		param_to = datetime.datetime.fromtimestamp(param_to)
		logging.info(param_from)
		logging.info(param_to)
		graphData = EmailModel.get_count_statistic_by_dates(param_from, param_to)
		context = {
			'week': graphData,
		}
		logging.info(context)
		self.response.write(json.dumps(context))
