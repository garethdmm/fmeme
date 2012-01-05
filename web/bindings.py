from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app 

from home import HomeHandler
from bake import BakeHandler
from image import ImageHandler
from fbshare import FBShareHandler

appRoute = webapp.WSGIApplication( [
  ('/', HomeHandler),
  ('/bake', BakeHandler),
  ('/image', ImageHandler),
  ('/fbshare', FBShareHandler),
], debug=True)

def main():
  run_wsgi_app(appRoute)

if __name__ == '__main__':
  main()
