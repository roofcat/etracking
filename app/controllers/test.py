# -*- coding: utf-8 -*-
#!/usr/bin/env python


import webapp2
import json
import logging
import base64
import re
import datetime
import mimetypes
import tablib
import StringIO


from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor


from app.models.email import EmailModel
from app.models.email import AttachModel
from app.models.email import JSONEncoder
from config.jinja_environment import JINJA_ENVIRONMENT


class RenderIndexTestHandler(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template("test/index.html")
        self.response.write(template.render())


class QueriesHandler(webapp2.RequestHandler):
    """ Probando paginación """

    def get(self):
        sEcho = self.request.get('sEcho')
        sEcho = int(sEcho, base=10)
        logging.info(sEcho)
        iDisplayStart = self.request.get('iDisplayStart')
        iDisplayStart = int(iDisplayStart, base=10)
        logging.info('iDisplayStart')
        logging.info(iDisplayStart)
        iDisplayLength = self.request.get('iDisplayLength')
        iDisplayLength = int(iDisplayLength, base=10)
        logging.info('iDisplayLength')
        logging.info(iDisplayLength)
        iSortCol_0 = self.request.get('iSortCol_0')
        logging.info(iSortCol_0)
        iSortingCols = self.request.get('iSortingCols')
        logging.info(iSortingCols)
        sSearch = self.request.get('sSearch')
        logging.info(sSearch)
        aColumns = self.request.get('aColumns')
        logging.info(aColumns)
        query = EmailModel.query()
        query = query.order(-EmailModel.input_datetime)
        iTotalRecords = query.count()
        query = query.fetch(iDisplayLength, offset=iDisplayStart)
        iTotalDisplayRecords = len(query)
        logging.info("iTotalDisplayRecords")
        logging.info(iTotalDisplayRecords)
        context = {
            'sEcho': sEcho,
            'aaData': JSONEncoder().default(query),
            #'iTotalDisplayRecords': iTotalDisplayRecords,
            'iTotalDisplayRecords': iTotalRecords,
            'iTotalRecords': iTotalRecords,
        }
        logging.info(context['sEcho'])
        logging.info(context['iTotalDisplayRecords'])
        logging.info(context['iTotalRecords'])
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(context))


class Queries2Handler(webapp2.RequestHandler):

    def get(self):
        logging.info(self.request.body)
        curs = Cursor(urlsafe=self.request.get('cursor_param'))
        query = EmailModel.query()
        emails, next_curs, more = query.fetch_page(50, start_cursor=curs)
        emails_array = []
        next_urlsafe = ''

        for email in emails:
            emails_array.append(JSONEncoder().default(email))

        if more and next_curs:
            next_urlsafe = next_curs.urlsafe()
        context = {
            'more': more,
            'next': next_urlsafe,
            'data': emails_array,
        }
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(context))


class TestInputWithUserAndPassword(webapp2.RequestHandler):

    def get(self):
        logging.info(self.request.headers)
        logging.info(self.request.body)
        headers = self.request.headers
        auth = headers['Authorization']
        logging.info(auth)
        auth = re.sub('^Basic ', '', auth)
        user, password = base64.decodestring(auth).split(':')
        logging.info(user)
        logging.info(password)
