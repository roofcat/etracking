# encoding: utf-8
#!/usr/bin/env python


import webapp2


from app.controllers.dtecontroller import Formulario
from app.controllers.dtecontroller import InputEmailHandler
from app.controllers.trackemailcontroller import EmailTrackHandler


app = webapp2.WSGIApplication([
	('/', Formulario),
    ('/input', InputEmailHandler),
    ('/track', EmailTrackHandler),
], debug=True)
