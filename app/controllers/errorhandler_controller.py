# -*- coding: utf-8 -*-
#!/usr/bin/env python


import webapp2
import logging


from config.jinja_environment import JINJA_ENVIRONMENT


def handle_404(request, response, exception):
	logging.exception(exception)
	template = JINJA_ENVIRONMENT.get_template('404.html')
	response.write(template.render())
	response.set_status(404)


def handle_403(request, response, exception):
	logging.exception(exception)
	template = JINJA_ENVIRONMENT.get_template('403.html')
	response.write(template.render())
	response.set_status(403)


def handle_500(request, response, exception):
	logging.exception(exception)
	template = JINJA_ENVIRONMENT.get_template('500.html')
	response.write(template.render())
	response.set_status(500)