# -*- coding: utf-8 -*-

import cgi
import os
from time import strftime
import time
import datetime

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
        
        len_bd = max_sp.Max_sp.all().count()
              
        bovespa_query = bovespa.Bovespa.all().order('-date')
        _bovespa = bovespa_query.fetch(len_bd - 1)

        _bovespa = [item.value for item in _bovespa]
        
        dollar_query = dollar.Dollar.all().order('-date')
        _dollar = dollar_query.fetch(len_bd - 1)

        _dollar = [item.value for item in _dollar]
        
        dowjones_query = dowjones.Dowjones.all().order('-date')
        _dowjones = dowjones_query.fetch(len_bd - 1)

        _dowjones = [item.value for item in _dowjones]
        
        max_sp_query = max_sp.Max_sp.all().order('-date')
        _max_sp = max_sp_query.fetch(len_bd)

        _max_sp = [item.value for item in _max_sp]
        
        nasdaq_query = nasdaq.Nasdaq.all().order('-date')
        _nasdaq = nasdaq_query.fetch(len_bd - 1)

        _nasdaq = [item.value for item in _nasdaq]

        petr4_query = petr4.Petr4.all().order('-date')
        _petr4 = petr4_query.fetch(len_bd - 1)

        _date = [datetime.date(int(p.date[:4]), int(p.date[4:6]), int(p.date[6:])).strftime('%d-%b') for p in _petr4]

        _petr4 = [item.value for item in _petr4]

        pearson_report  = stats.make_sunny_report(pearsonr, [_nasdaq, _bovespa, _dollar, _dowjones, _max_sp[:-1], _petr4], \
                                                  4, ['Nasdaq', 'Bovespa', 'USD/BRL exchange', 'Dow Jones', 'São Paulo\'s high forecast', 'PETR4 stocks'])
        spearman_report = stats.make_sunny_report(spearmanr,[_nasdaq, _bovespa, _dollar, _dowjones, _max_sp[:-1], _petr4], \
                                                  4, ['Nasdaq', 'Bovespa', 'USD/BRL exchange', 'Dow Jones', 'São Paulo\'s high forecast', 'PETR4 stocks'])

        p_idx = pearson_report['values'].index(max(pearson_report['values']))
        s_idx = spearman_report['values'].index(max(spearman_report['values']))

        template_values = {
          'date' : strftime('Today is day %d of month %m'),
          'bovespa' : int(_bovespa[0]),
          'dollar' : _dollar[0],
          'dowjones' : int(_dowjones[0]),
          'max_sp' : int(_max_sp[0]),
          'nasdaq' : int(_nasdaq[0]),
          'bovespa_list' : _bovespa,
          'dollar_list' : _dollar,
          'dow_jones_list' : _dowjones,
          'max_sp_list' : _max_sp[:-1],
          'nasdaq_list' : _nasdaq,
          'petr4_list' : _petr4,
          'bovespa_max' : max(_bovespa),
          'dollar_max' : max(_dollar),
          'dow_jones_max' : max(_dowjones),
          'max_sp_max' : max(_max_sp[:-1]),
          'nasdaq_max' : max(_nasdaq),
          'petr4_max' : max(_petr4),
          'bovespa_min' : min(_bovespa),
          'dollar_min' : min(_dollar),
          'dow_jones_min' : min(_dowjones),
          'max_sp_min' : min(_max_sp[:-1]),
          'nasdaq_min' : min(_nasdaq),
          'petr4_min' : min(_petr4),
          'date_list' : _date,
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
    

class bulkdelete(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        try:
            while True:
              nothing = True
              for key in ['Bovespa', 'Dollar', 'Dowjones', 'Max_sp', 'Nasdaq', 'Petr4']:
                q = db.GqlQuery('SELECT __key__ FROM ' + key)
                if q.count():
                  nothing = False
                  db.delete(q.fetch(200))
                  time.sleep(0.5)
              if nothing:
                assert 0
        except Exception, e:
            self.response.out.write(repr(e)+'\n')
            pass

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/cron/update', Cron),
                                      ('/clean', bulkdelete)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
