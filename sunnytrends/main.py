# -*- coding: utf-8 -*-

import cgi
import os
from time import strftime

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from deps.statlib.stats import *

import bovespa
import dollar
import dowjones
import max_sp
import nasdaq
import petr4

import stats


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

        petr4_query = petr4.Petr4.all().order('-date')
        _petr4 = petr4_query.fetch(10)

        pearson_report  = stats.make_report(pearsonr, [_nasdaq, _bovespa, _dollar, _dowjones, _max_sp[:-1], _petr4])
        spearman_report = stats.make_report(spearmanr,[_nasdaq, _bovespa, _dollar, _dowjones, _max_sp[:-1], _petr4])        

        p_idx = pearson_report['values'].index(max(pearson_report['values']))
        s_idx = spearman_report['values'].index(max(spearman_report['values']))

        template_values = {
          'date' : strftime('Today is day %d of month %m'),
          'bovespa' : int(_bovespa[0].value),
          'dollar' : _dollar[0].value,
          'dowjones' : int(_dowjones[0].value),
          'max_sp' : int(_max_sp[0].value),
          'nasdaq' : int(_nasdaq[0].value),
          'bovespa_list' : _bovespa,
          'dollar_list' : _dollar,
          'dow_jones_list' : _dowjones,
          'max_sp_list' : _max_sp[:-1],
          'nasdaq_list' : _nasdaq,
          'petr4_list' : _petr4,
          'max_linear_correl' : [pearson_report[key][p_idx] for key in sorted(pearson_report.keys())],
          'max_rank_correl' : [spearman_report[key][p_idx] for key in sorted(spearman_report.keys())]
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
