# -*- coding: utf-8 -*-
#!/usr/bin/env python

import logging
import mimetypes


import webapp2
from google.appengine.ext import ndb


from app_controller import BaseHandler


class FindAttachHandler(BaseHandler):
    """ Clase que controla los link de documentos adjuntos
            de un correo enviado por un dte
    """

    def get(self, file_id):
        if file_id:
            try:
                file_id = str(file_id)
                attach = ndb.Key(urlsafe=file_id).get()
                self.response.headers['Content-Type'] = mimetypes.guess_type(attach.nombre)[0]
                self.response.headers['Content-Disposition'] = 'attachment; filename=' + attach.nombre
                self.response.write(attach.archivo)
            except Exception, e:
                logging.error(e)
        else:
            self.error(404)


class FindReportHandler(webapp2.RequestHandler):
    """ Clase que controla las busquedas de links
            de reportes generados por las colas y enviados
            a los usuarios por email
    """

    def get(self, file_id):
        if file_id:
            try:
                file_id = str(file_id)
                report = ndb.Key(urlsafe=file_id).get()
                self.response.headers['Content-Type'] = 'application/xlsx'
                self.response.headers['Content-Disposition'] = 'attachment; filename=' + str(report.name)
                self.response.write(report.export_file)
            except Exception, e:
                logging.error(e)
        else:
            self.error(404)
