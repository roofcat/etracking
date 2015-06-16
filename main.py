# -*- coding: utf-8 -*-
#!/usr/bin/env python


import webapp2


# imports para servicios rest DTE
from app.controllers.dteinput_controller import InputEmailHandler
from app.controllers.dteinput_controller import InputEmailQueueHandler
from app.controllers.webhook_controller import SendrigWebhookHandler

# imports para admin
from app.controllers.oauth_controller import AuthHandler
from app.controllers.oauth_controller import RevokeHandler
from app.controllers.admin_controller import AdminHandler
from app.controllers.statistic_controller import IndexStatisticHandler
from app.controllers.statistic_controller import GraphStatisticHandler
from app.controllers.user_controller import UserAdminHandler
from app.controllers.user_controller import ListUserAdminHandler
from app.controllers.user_controller import NewUserAdminHandler

from app.controllers.panel_controller import HomePanelHandler

# manejo de errores
from app.controllers.errorhandler_controller import handle_404
from app.controllers.errorhandler_controller import handle_500

# imports para pruebas
from app.controllers.test import TestHandler
from app.controllers.test import TestInputWithUserAndPassword


# Decorador para oauth2
from config.oauth2_utils import decorator


app = webapp2.WSGIApplication([
	(r'/', HomePanelHandler),
	(r'/admin', AdminHandler),
	(r'/admin/statistics', IndexStatisticHandler),
	(r'/admin/statistics/stats', GraphStatisticHandler),
	(r'/admin/users', UserAdminHandler),
	(r'/admin/users/list', ListUserAdminHandler),
	(r'/admin/users/new', NewUserAdminHandler),

	#Eliminar token para el admin azurian
	(r'/revoke', RevokeHandler),
	(r'/home', HomePanelHandler),
    (r'/input', InputEmailHandler),
    (r'/inputqueue', InputEmailQueueHandler),
    (r'/webhook', SendrigWebhookHandler),
    (r'/test', TestHandler),
    (r'/testauth', TestInputWithUserAndPassword),
    (decorator.callback_path, decorator.callback_handler()),
], debug=True)

#app.error_handlers[404] = handle_404
#app.error_handlers[500] = handle_500