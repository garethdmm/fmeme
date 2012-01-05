from google.appengine.ext import webapp

class FBShareHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write('<script type="text/javascript">window.opener.childopen()</script><img src=\'images/loading.gif\' style=\'display: block; margin-left: auto; margin-top: 150px; margin-right: auto;\'/>')
