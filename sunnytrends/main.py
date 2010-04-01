# -*- coding: utf-8 -*-

import cgi
import os
from time import strftime

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

class MainPage(webapp.RequestHandler):
    def get(self):
        bovespa_query = bovespa.Bovespa.all().order('-date')
        _bovespa = bovespa_query.fetch(10)
        
        dollar_query = dollar.Dollar.all().order('-date')
        _dollar = dollar_query.fetch(10)
        
        dowjones_query = dowjones.Dowjones.all().order('-date')
        _dowjones = dowjones_query.fetch(10)
        
        max_sp_query = max_sp.Max_sp.all().order('-date')
        _max_sp = max_sp_query.fetch(11)
        
        nasdaq_query = nasdaq.Nasdaq.all().order('-date')
        _nasdaq = nasdaq_query.fetch(10)
    
        template_values = {
          'date' : strftime('Hoje é o dia %d do mês %m do ano de %Y'),
          'bovespa' : _bovespa[0],
          'dollar' : _dollar[0],
          'dowjones' : _dowjones[0],
          'max_sp' : _max_sp[0],
          'nasdaq' : _nasdaq[0],
          'bovespa_list' : _bovespa,
          'dollar_list' : _dollar,
          'dow_jones_list' : _dowjones,
          'max_sp_list' : _max_sp[:-1],
          'nasdaq_list' : _nasdaq,
          }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class Cron(webapp.RequestHandler):
    def get(self):
        report = cron.main()
        template_values = {'report': report}
        path = os.path.join(os.path.dirname(__file__), 'cron.html')
        self.response.out.write(template.render(path, template_values))        
    

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/cron/update', Cron)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
