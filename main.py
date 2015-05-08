# encoding: utf-8
#!/usr/bin/env python


import webapp2


from app.controllers.dteinput_controller import InputEmailHandler
from app.controllers.trackemail_controller import EmailTrackHandler
from app.controllers.bounce_controller import EmailClientBounceHandler
from app.controllers.inboundmail_controller import EmailClientInboundHandler
from app.controllers.sendgrid_webhook import SendrigWebhookHandler


app = webapp2.WSGIApplication([
    ('/input', InputEmailHandler),
    ('/track', EmailTrackHandler),
    ('/webhook', SendrigWebhookHandler),
    EmailClientBounceHandler.mapping(),
    EmailClientInboundHandler.mapping(),
], debug=True)
