# -*- coding: utf-8 -*-
#!/usr/bin/env python


import webapp2
import logging
import datetime


from google.appengine.api import taskqueue


from app.models.email import EmailModel


class SendLaggingCronHandler(webapp2.RequestHandler):

	def get(self):
		query = EmailModel.get_email_lagging()
		for qry in query:
			context = {
                'correo': qry.correo,
                'numero_folio': qry.numero_folio,
                'tipo_dte': qry.tipo_dte,
          	}
			# Inicio taskqueue
			q = taskqueue.Queue('InputQueue')
			t = taskqueue.Task(url='/inputqueue', params=context)
			q.add(t)