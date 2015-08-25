# -*- coding: utf-8 -*-
#!/usr/bin/env python


import webapp2
import webapp2_extras


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


# imports para usuarios normales
from app.controllers.panel_controller import LoginPanelHandler
from app.controllers.panel_controller import LogoutPanelHandler
from app.controllers.panel_controller import HomePanelHandler
from app.controllers.panel_controller import EmailPanelHandler
from app.controllers.panel_controller import FolioPanelHandler
from app.controllers.panel_controller import RutReceptorPanelHandler


# imports para reportes csv
from app.controllers.csv_controller import ExportHomePanelHandler


# import tareas cron
from app.controllers.cron_controller import SendLaggingCronHandler


# import para uso de apis
from app.controllers.panel_controller import StatisticPanelHandler
from app.controllers.panel_controller import StatisticEmailPanelHandler


# manejo de errores
from app.controllers.errorhandler_controller import handle_403
from app.controllers.errorhandler_controller import handle_404
from app.controllers.errorhandler_controller import handle_500


# imports para pruebas
from app.controllers.test import TestHandler
from app.controllers.test import Test2Handler
from app.controllers.test import Test3Handler
from app.controllers.test import Test4Handler
from app.controllers.test import Test5Handler
from app.controllers.test import TestInputWithUserAndPassword


# Decorador para oauth2
from config.oauth2_utils import decorator


config = {}
config['webapp2_extras.sessions'] = {'secret_key': 'EstaEsMiSuperKey', }


app = webapp2.WSGIApplication([
    # panel usuario clientes
    (r'/', HomePanelHandler),
    (r'/email/$', EmailPanelHandler),
    (r'/folio/$', FolioPanelHandler),
    (r'/receptor/$', RutReceptorPanelHandler),

    # rutas para descargar csv
    (r'/export/stats/(\d+)/(\d+)/(.+)/$', ExportHomePanelHandler),
    
    # url apis
    (r'/api/statistics/globalstats/(\d+)/(\d+)/(.+)/$', StatisticPanelHandler),
    (r'/api/statistics/email/$', StatisticEmailPanelHandler),

    # tareas cron
    (r'/cron/sendlagging/$', SendLaggingCronHandler),
    
    # autenticacion
    (r'/login/$', LoginPanelHandler),
    (r'/logout/$', LogoutPanelHandler),

    # panel admin azurian
    (r'^/admin/$', AdminHandler),
    (r'^/admin/statistics/$', IndexStatisticHandler),
    (r'^/admin/statistics/stats/$', GraphStatisticHandler),
    (r'^/admin/users/$', UserAdminHandler),
    (r'^/admin/users/list/$', ListUserAdminHandler),
    (r'^/admin/users/new/$', NewUserAdminHandler),

    # Eliminar token para el admin azurian
    (r'^/revoke/$', RevokeHandler),
    (r'^/home/$', HomePanelHandler),
    (r'^/input/$', InputEmailHandler),
    (r'^/inputqueue', InputEmailQueueHandler),
    (r'^/webhook/$', SendrigWebhookHandler),
    (r'/test1', TestHandler),
    (r'/test2', Test2Handler),
    (r'/test3', Test3Handler),
    (r'/test4', Test4Handler),
    (r'/test5', Test5Handler),
    (r'/testauth', TestInputWithUserAndPassword),
    (decorator.callback_path, decorator.callback_handler()),
], config=config, debug=True)

app.error_handlers[403] = handle_403
app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500
