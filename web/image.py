from google.appengine.ext import webapp

import urllib
import base64
import logging

class ImageHandler(webapp.RequestHandler):
  def get(self):
    # receive image bytes
    image_id = self.request.get('id', '' )
    meme_name = self.request.get('meme_name', '')

    imgur_link = 'http://i.imgur.com/' + image_id

    params = {
      'title': meme_name,
      'image_url': imgur_link,
      'page_url': self.request.url,
    }

    template = open('static/html/image.html').read()

    self.response.out.write(template % params)

  def post(self):
    # receive image bytes
    image_id = self.request.get('id', '' )
    meme_name = self.request.get('meme_name', '')

    imgur_link = 'http://i.imgur.com/' + image_id

    params = {
      'title': meme_name,
      'image_url': imgur_link,
      'page_url': self.request.url,
    }

    template = open('static/html/image.html').read()

    self.response.out.write(template % params)
