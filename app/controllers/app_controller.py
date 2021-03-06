# -*- coding: utf-8 -*-
#!/usr/bin/env python


import webapp2
from webapp2_extras import sessions
import logging


class BaseHandler(webapp2.RequestHandler):

    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        except Exception, e:
            logging.error(e)
            self.redirect('/logout/')
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()
