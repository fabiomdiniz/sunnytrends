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

class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
    def get(self):
        bovespa_query = bovespa.Bovespa.all().order('-date')
        _bovespa = bovespa_query.fetch(1)
        
        dollar_query = dollar.Dollar.all().order('-date')
        _dollar = dollar_query.fetch(1)
        
        dowjones_query = dowjones.Dowjones.all().order('-date')
        _dowjones = dowjones_query.fetch(1)
        
        max_sp_query = max_sp.Max_sp.all().order('-date')
        _max_sp = max_sp_query.fetch(1)
        
        nasdaq_query = nasdaq.Nasdaq.all().order('-date')
        _nasdaq = nasdaq_query.fetch(1)
    
        greetings_query = Greeting.all().order('-date')
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
          'date' : strftime('Hoje é o dia %d do mês %m do ano de %Y'),
          'bovespa' : _bovespa,
          'dollar' : _dollar,
          'dowjones' : _dowjones,
          'max_sp' : _max_sp,
          'nasdaq' : _nasdaq,
          'greetings': greetings,
          'url': url,
          'url_linktext': url_linktext,
          }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class Guestbook(webapp.RequestHandler):
    def post(self):
        greeting = Greeting()

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/')

class Cron(webapp.RequestHandler):
    def get(self):
        report = cron.main()
        template_values = {'report': report}
        path = os.path.join(os.path.dirname(__file__), 'cron.html')
        self.response.out.write(template.render(path, template_values))        
    

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', Guestbook),
                                      ('/cron/update', Cron)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
