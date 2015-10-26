# -*- coding: utf-8 -*-
#!/usr/bin/env python


import webapp2
import webapp2_extras


# imports para servicios rest DTE
from app.controllers.dteinput_controller import InputEmailHandler
from app.controllers.dteinput_controller import InputEmailQueueHandler
from app.controllers.webhook_rest_controller import SendgridWebhookApiRestHandler
from app.controllers.webhook_api_controller import SendgridWebhookAPIHandler


# imports para admin
from app.controllers.oauth_controller import AuthHandler
from app.controllers.oauth_controller import RevokeHandler
from app.controllers.admin_controller import AdminHandler
from app.controllers.statistic_controller import IndexStatisticHandler
from app.controllers.statistic_controller import GraphStatisticHandler
from app.controllers.user_admin_controller import UserAdminHandler
from app.controllers.user_admin_controller import ListUserAdminHandler
from app.controllers.user_admin_controller import NewUserAdminHandler


# imports para usuarios normales
from app.controllers.user_profile_controller import LoginPanelHandler
from app.controllers.user_profile_controller import LogoutPanelHandler
from app.controllers.user_profile_controller import ProfilePanelHandler
from app.controllers.user_profile_controller import UpdateProfilePanelHandler
from app.controllers.user_profile_controller import UpdatePasswordProfilePanelHandler
from app.controllers.panel_controller import DashboardHandler
from app.controllers.panel_controller import CustomSearchHandler


# Imports para adjuntos
from app.controllers.attach_controller import FindAttachHandler
from app.controllers.attach_controller import FindReportHandler


# imports para reportes csv
from app.controllers.export_controller import QueueExportHandler
from app.controllers.export_controller import ExportGeneralEmailHandler
from app.controllers.export_controller import ExportSendedEmailHandler
from app.controllers.export_controller import ExportFailureEmailHandler
from app.controllers.export_controller import ExportSearchByEmailHandler
from app.controllers.export_controller import ExportSearchByFolioHandler
from app.controllers.export_controller import ExportSearchByRutHandler
from app.controllers.export_controller import ExportSearchByFailureHandler
from app.controllers.export_controller import ExportSearchByMountHandler


# import para uso de apis
from app.controllers.panel_controller import StatisticPanelHandler
from app.controllers.panel_controller import EmailSearchHandler
from app.controllers.panel_controller import FolioSearchHandler
from app.controllers.panel_controller import RutReceptorSearchHandler
from app.controllers.panel_controller import FallidosSearchHandler
from app.controllers.panel_controller import MontosSearchHandler


# import tareas cron
from app.controllers.cron_controller import SendLaggingCronHandler
from app.controllers.cron_controller import CleanExportHandler


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
from app.controllers.test import TestViewFileHandler
from app.controllers.test import TestInputWithUserAndPassword
from app.controllers.test import TabLibHandler
from app.controllers.test import QueriesHandler


# Decorador para oauth2
from config.oauth2_utils import decorator


config = {}
config['webapp2_extras.sessions'] = {'secret_key': 'EstaEsMiSuperKey', }


app = webapp2.WSGIApplication([
    # panel usuario clientes
    (r'/', DashboardHandler),
    (r'/customsearch/$', CustomSearchHandler),
    (r'/profile/$', ProfilePanelHandler),

    # rutas para descargar csv
    (r'/export/general/(\d+)/(\d+)/(.+)/$', ExportGeneralEmailHandler),
    (r'/export/sended/(\d+)/(\d+)/(.+)/$', ExportSendedEmailHandler),
    (r'/export/failure/(\d+)/(\d+)/(.+)/$', ExportFailureEmailHandler),
    (r'/export/email/(\d+)/(\d+)/(.+)/$', ExportSearchByEmailHandler),
    (r'/export/folio/(\d+)/$', ExportSearchByFolioHandler),
    (r'/export/rut/(\d+)/(\d+)/(.+)/$', ExportSearchByRutHandler),
    (r'/export/fallidos/(\d+)/(\d+)/$', ExportSearchByFailureHandler),
    (r'/export/montos/(\d+)/(\d+)/(\d+)/(\d+)/$', ExportSearchByMountHandler),

    # api entrada
    (r'/api/input/$', InputEmailHandler),
    (r'/api/webhook-rest/$', SendgridWebhookApiRestHandler),
    (r'/api/webhook-api/$', SendgridWebhookAPIHandler),

    # api estadisticas
    (r'/api/statistics/globalstats/(\d+)/(\d+)/(.+)/$', StatisticPanelHandler),

    # api busquedas
    (r'/api/search/email/(\d+)/(\d+)/(.+)/$', EmailSearchHandler),
    (r'/api/search/folio/(.+)/$', FolioSearchHandler),
    (r'/api/search/rut/(\d+)/(\d+)/(.+)/$', RutReceptorSearchHandler),
    (r'/api/search/fallidos/(\d+)/(\d+)/$', FallidosSearchHandler),
    (r'/api/search/montos/(\d+)/(\d+)/(\d+)/(\d+)/$', MontosSearchHandler),
    
    # api actualizacion de datos usuario final
    (r'/api/profile/user/update/$', UpdateProfilePanelHandler),
    (r'/api/profile/user/password/$', UpdatePasswordProfilePanelHandler),

    # Link a archivos del datastore
    (r'/storage/attach/(.+)/', FindAttachHandler),
    (r'/storage/report/(.+)/', FindReportHandler),

    # tareas cron
    (r'/cron/sendlagging/$', SendLaggingCronHandler),
    (r'/cron/cleanexport/$', CleanExportHandler),
    
    # autenticacion
    (r'/login/$', LoginPanelHandler),
    (r'/logout/$', CleanExportHandler),

    # panel admin azurian
    (r'/admin/$', AdminHandler),
    (r'/admin/statistics/$', IndexStatisticHandler),
    (r'/admin/statistics/stats/$', GraphStatisticHandler),
    (r'/admin/users/$', UserAdminHandler),
    (r'/admin/users/list/$', ListUserAdminHandler),
    (r'/admin/users/new/$', NewUserAdminHandler),

    # Rutas de colas de tareas
    (r'/inputqueue', InputEmailQueueHandler),
    (r'/exportqueue', QueueExportHandler),

    # Eliminar token para el admin azurian
    (r'/revoke/$', RevokeHandler),
    (r'/test1', TestHandler),
    # (r'/xlsx', TabLibHandler),
    # (r'/test2', Test2Handler),
    # (r'/test3', Test3Handler),
    # (r'/test4', Test4Handler),
    # (r'/test5', Test5Handler),
    # (r'/test-file/(.+)/$', TestViewFileHandler),
    # (r'/testauth', TestInputWithUserAndPassword),
    (r'/testqueries', QueriesHandler),
    (decorator.callback_path, decorator.callback_handler()),
], config=config, debug=True)

# Handlers para errores comunes
app.error_handlers[403] = handle_403
app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500
