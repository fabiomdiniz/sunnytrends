# -*- coding: utf-8 -*-

from google.appengine.ext import db
from time import strftime
import urllib
from deps.BeautifulSoup import BeautifulSoup

class Petr4(db.Model):
  value = db.FloatProperty()
  date = db.StringProperty()

def get():
    html = urllib.urlopen('http://br.finance.yahoo.com/q?s=petr4.SA')
    soup = BeautifulSoup(html)
    return [float(soup.big.b.string[:-3].replace(',', '')), strftime('%Y%m%d')]

