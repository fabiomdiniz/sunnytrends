# -*- coding: utf-8 -*-

from google.appengine.ext import db
from time import strftime
import urllib
import os

class Dollar(db.Model):
  value = db.FloatProperty()
  date = db.StringProperty()

def get():
    return [float(urllib.urlopen('http://download.finance.yahoo.com/d/quotes.csv?s=USDBRL=X&f=sl1&e=.csv').read().split(',')[-1].rstrip()), strftime('%Y%m%d')]