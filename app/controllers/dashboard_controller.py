# -*- coding: utf-8 -*-
#!/usr/bin/env python


import datetime
import json
import logging


from app_controller import BaseHandler
from app.models.email import EmailModel
from app.models.email import JSONEncoder
from config.jinja_environment import JINJA_ENVIRONMENT


class DashboardHandler(BaseHandler):

    def get(self):
        user = None
        try:
            user = self.session['user']
        except:
            self.redirect('/login/')
        if user:
            context = { 'data': user, }
            template = JINJA_ENVIRONMENT.get_template('panel/index.html')
            self.response.write(template.render(context))


class StatisticPanelHandler(BaseHandler):

    def get(self, date_from, date_to, options):

        if date_from and date_to and options:
            date_from = int(date_from)
            date_to = int(date_to)
            date_from = datetime.datetime.fromtimestamp(date_from)
            date_to = datetime.datetime.fromtimestamp(date_to)
            # busqueda de datos
            data = EmailModel.get_statistic_by_dates(date_from, date_to, options)
            results = EmailModel.get_stats_by_dates(date_from, date_to, options)
            context = {
                'date_from': str(date_from),
                'date_to': str(date_to),
                'statistic': data,
                'results': results,
            }
            self.response.write(json.dumps(context))
