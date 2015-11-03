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
        PAGE_LENGTH = 50
        logging.info(self.request.body)
        secho = self.request.get('sEcho')
        logging.info(secho)
        display_start = self.request.get('iDisplayStart')
        logging.info(display_start)
        display_length = self.request.get('iDisplayLength')
        logging.info(display_length)
        sort_col = self.request.get('iSortCol_0')
        logging.info(sort_col)
        sort_dir = self.request.get('iSortDir_0')
        logging.info(sort_dir)
        search = self.request.get('sSearch')
        logging.info(search)
        if display_start:
            display_start = int(display_start, base=10)
        else:
            display_start = 1
        if display_length:
            display_length = int(display_length, base=10)
        offset = PAGE_LENGTH * display_start
        logging.info(offset)
        query = EmailModel.query()
        query = query.order(-EmailModel.input_date)
        recordsTotal = query.count()
        query = query.fetch(PAGE_LENGTH, offset=offset)
        data = []
        for q in query:
            data.append(JSONEncoder().default(q))
        context = {
            'aaData': data,
            'iTotalDisplayRecords': display_length,
            'iTotalRecords': recordsTotal,
        }
        logging.info(context)
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
