# -*- coding: utf-8 -*-
#!/usr/bin/env python

import logging
import mimetypes
from google.appengine.ext import ndb


from app_controller import BaseHandler


class FindAttachHandler(BaseHandler):

	def get(self, file_id):
		if file_id:
			try:
				file_id = str(file_id)
				attach = ndb.Key(urlsafe=file_id).get()
				self.response.headers['Content-Type'] = mimetypes.guess_type(attach.nombre)[0]
				self.response.write(attach.archivo)
			except Exception, e:
				logging.error(e)
		else:
			self.error(404)