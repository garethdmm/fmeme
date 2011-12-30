from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app 

from home import HomeHandler
from bake import BakeHandler

appRoute = webapp.WSGIApplication( [
  ('/', HomeHandler),
  ('/bake', BakeHandler),
], debug=True)

def main():
  run_wsgi_app(appRoute)

if __name__ == '__main__':
  main()
