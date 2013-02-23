# -*- coding: utf-8 -*-

from google.appengine.ext import db
from time import strftime
import urllib
from deps.BeautifulSoup import BeautifulSoup


class Dowjones(db.Model):
    value = db.FloatProperty()
    date = db.StringProperty()


def get():
    url = 'http://finance.yahoo.com/q?s=indu'
    soup = BeautifulSoup(urllib.urlopen(url))
    value = float(soup('span', attrs={'id': 'yfs_l10_^dji'})[0].text.replace(',', ''))
    return [value, strftime('%Y%m%d')]
