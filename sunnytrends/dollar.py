# -*- coding: utf-8 -*-

from google.appengine.ext import db
from time import strftime
import urllib
import os
from deps.BeautifulSoup import BeautifulSoup

class Dollar(db.Model):
  value = db.FloatProperty()
  date = db.StringProperty()

def get():
    html = urllib.urlopen('http://br.finance.yahoo.com/currency/convert?amt=1&from=USD&to=BRL')
    soup = BeautifulSoup(html)
    return [float(soup('b')[-5].string.replace(',','.')), strftime('%Y%m%d')]
