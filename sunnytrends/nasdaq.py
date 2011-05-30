# -*- coding: utf-8 -*-

from google.appengine.ext import db
from time import strftime
import urllib
from deps import ystockquote

class Nasdaq(db.Model):
  value = db.FloatProperty()
  date = db.StringProperty()

def get():
    return [float(ystockquote.get_price('^IXIC')), strftime('%Y%m%d')]
