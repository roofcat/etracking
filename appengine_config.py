"""
Este archivo linkea librerias externas que no trae por
defecto la plataforma de Google App Engine
"""
from google.appengine.ext import vendor


vendor.add('vendor')