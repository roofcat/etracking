# -*- coding: utf-8 -*-
#!/usr/bin/env python


import webapp2
import logging
from datetime import datetime, time, date, timedelta


from google.appengine.api import taskqueue


from app.models.email import EmailModel
from app.models.export import ExportModel


class SendLaggingCronHandler(webapp2.RequestHandler):

	def get(self):
		query = EmailModel.get_email_lagging()
		if query:
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
		else:
			self.response.write("nada que enviar")


class CleanExportHandler(webapp2.RequestHandler):

	def get(self):
		day = timedelta(days=1)
		today = datetime.now()
		yesterday = today - day
		query = ExportModel.query()
		query = query.filter(ExportModel.input_date == yesterday)
		query = query.fetch()
		if query:
			for row in query:
				row.key.delete()
			self.response.write("Limpieza de ExportModel OK" + len(query))
		else:
			self.response.write("No habían registro que eliminar")
