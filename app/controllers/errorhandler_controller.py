# encoding: utf-8
#!/usr/bin/env python


import webapp2


from config.jinja_environment import JINJA_ENVIRONMENT


def handle_404(request, response, exception):
	template = JINJA_ENVIRONMENT.get_template('404.html')
	response.write(template.render())


def handle_500(request, response, exception):
	template = JINJA_ENVIRONMENT.get_template('500.html')
	response.write(template.render())