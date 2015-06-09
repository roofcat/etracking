# -*- coding: utf-8 -*-
#!/usr/bin/env python


import webapp2


from app.controllers.dteinput_controller import InputEmailHandler
from app.controllers.dteinput_controller import InputEmailQueueHandler
from app.controllers.webhook_controller import SendrigWebhookHandler
from app.controllers.oauth_controller import AuthHandler
from app.controllers.oauth_controller import RevokeHandler
from app.controllers.panel_controller import HomePanelHandler
from app.controllers.errorhandler_controller import handle_404
from app.controllers.errorhandler_controller import handle_500
from app.controllers.test import TestHandler
from app.controllers.test import TestInputWithUserAndPassword
from config.oauth2_utils import decorator


app = webapp2.WSGIApplication([
	('/', AuthHandler),
	('/revoke', RevokeHandler),
	('/home', HomePanelHandler),
    ('/input', InputEmailHandler),
    ('/inputqueue', InputEmailQueueHandler),
    ('/webhook', SendrigWebhookHandler),
    ('/test', TestHandler),
    ('/testauth', TestInputWithUserAndPassword),
    (decorator.callback_path, decorator.callback_handler()),
], debug=True)

app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500