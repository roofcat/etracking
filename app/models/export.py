# -*- coding: utf-8 -*-
#!/usr/bin/env python


from google.appengine.ext import ndb


class ExportModel(ndb.Model):
	input_date = ndb.DateProperty(auto_now_add=True, indexed=True)
	name = ndb.StringProperty(indexed=True)
	export_file = ndb.BlobProperty()
	user = ndb.StringProperty(indexed=True)
