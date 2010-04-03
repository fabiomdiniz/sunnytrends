# -*- coding: utf-8 -*-

import cgi
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
import bovespa
import dollar
import dowjones
import max_sp
import nasdaq
import petr4

def update():
    report = {}
  
    _bovespa = bovespa.Bovespa()
    try:
        _bovespa.value, _bovespa.date = bovespa.get()
        _bovespa.put()
        report['bovespa'] = True
    except:
        report['bovespa'] = False
    
    _dollar = dollar.Dollar()
    try:
        _dollar.value, _dollar.date = dollar.get()
        _dollar.put()
        report['dollar'] = True
    except:
        report['dollar'] = False
    
    _dowjones = dowjones.Dowjones()
    try:
        _dowjones.value, _dowjones.date = dowjones.get()
        _dowjones.put()
        report['dowjones'] = True
    except:
        report['dowjones'] = False
    
    _max_sp = max_sp.Max_sp()
    try:
        _max_sp.value, _max_sp.date = max_sp.get()
        _max_sp.put()
        report['max_sp'] = True
    except:
        report['max_sp'] = False
    
    _nasdaq = nasdaq.Nasdaq()
    try:
        _nasdaq.value, _nasdaq.date = nasdaq.get()
        _nasdaq.put()
        report['nasdaq'] = True
    except:
        report['nasdaq'] = False

    _petr4 = petr4.Petr4()
    try:
        _petr4.value, _petr4.date = petr4.get()
        _petr4.put()
        report['petr4'] = True
    except:
        report['petr4'] = False
    
    return report

class Cron(webapp.RequestHandler):
    def get(self):
        report = update()
        template_values = {'report': report}
        path = os.path.join(os.path.dirname(__file__), 'cron.html')
        self.response.out.write(template.render(path, template_values))        
    

application = webapp.WSGIApplication(
                                     [('/cron/update', Cron)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
