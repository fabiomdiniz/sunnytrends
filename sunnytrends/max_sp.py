# -*- coding: utf-8 -*-

from google.appengine.ext import db
from datetime import datetime, timedelta
import urllib
import os
import xml.dom.minidom

class Max_sp(db.Model):
  value = db.FloatProperty()
  date = db.StringProperty()

def get():
    html = urllib.urlopen('http://xoap.weather.com/weather/local/BRXX0232?dayf=2&link=xoap&prod=xoap&par=1105827508&key=783abed588a1bdac&unit=m')
    dom = xml.dom.minidom.parseString(html.read())
    max_sp = float(dom.getElementsByTagName('hi')[1].firstChild.data)
    tomorrow = datetime.today() + timedelta(1)
    return [max_sp, str(tomorrow)[:10].replace('-','')]
