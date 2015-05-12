# encoding: utf-8
#!/usr/bin/env python


import webapp2


from app.controllers.dteinput_controller import InputEmailHandler
from app.controllers.dteinput_controller import InputEmailQueueHandler
from app.controllers.sendgrid_webhook import SendrigWebhookHandler


app = webapp2.WSGIApplication([
    ('/input', InputEmailHandler),
    ('/inputqueue', InputEmailQueueHandler),
    ('/webhook', SendrigWebhookHandler),
], debug=True)
