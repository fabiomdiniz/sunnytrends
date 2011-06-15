# -*- coding: utf-8 -*-

from google.appengine.ext import db
from time import strftime
import urllib
from deps import ystockquote as ys

class Bovespa(db.Model):
  value = db.FloatProperty()
  date = db.StringProperty()

def get():
    #return [float(ystockquote.get_price('^BVSP')), strftime('%Y%m%d')]
    return [float(ys.get_price('^BVSP')), strftime('%Y%m%d')]