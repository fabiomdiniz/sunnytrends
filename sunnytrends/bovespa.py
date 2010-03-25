# -*- coding: utf-8 -*-

from google.appengine.ext import db
from time import strftime
import urllib
from BeautifulSoup import BeautifulSoup

class Bovespa(db.Model):
  value = db.FloatProperty()
  date = db.StringProperty()

def get():
    html = urllib.urlopen('http://br.finance.yahoo.com/q?s=^BVSP')
    soup = BeautifulSoup(html)
    return [float(soup.big.b.string.replace(',', '')), strftime('%Y%m%d')]

