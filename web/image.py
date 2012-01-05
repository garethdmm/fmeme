from google.appengine.ext import webapp

import urllib
import base64
import logging

class ImageHandler(webapp.RequestHandler):
  def get(self):
    # receive image bytes
    image_id = self.request.get('id', '' )

    # render a page with basically just an image tag pointing to the
    # imgur link
    self.response.out.write("<img src='http://i.imgur.com/" + image_id + "'>")


