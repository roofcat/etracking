# encoding:utf-8
#!/usr/bin/env python

import jinja2
import os


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.abspath('app/views')),
    autoescape=True,
    extensions=['jinja2.ext.autoescape']
)

print JINJA_ENVIRONMENT.loader.__dict__