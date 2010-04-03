# -*- coding: utf-8 -*-

from google.appengine.ext import db
from time import strftime
import urllib
from deps.BeautifulSoup import BeautifulSoup

class Dowjones(db.Model):
  value = db.FloatProperty()
  date = db.StringProperty()

def get():
    html = urllib.urlopen('http://br.finance.yahoo.com/q?s=^DJI')
    soup = BeautifulSoup(html)
    return [float(soup.big.b.string.replace(',', '')), strftime('%Y%m%d')]

