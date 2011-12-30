from google.appengine.ext import webapp


class BakeHandler(webapp.RequestHandler):
  def post(self):
    """
    1) Create Image and save
    2) Return url
    """

    self.response.out.write('http://i.qkme.me/35llpl.jpg')
    return
