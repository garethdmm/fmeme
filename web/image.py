from google.appengine.ext import webapp

from model import Image
from constants import meme_names, meme_default_links

import urllib
import base64
import logging

class ImageHandler(webapp.RequestHandler):
  def get(self):
    # receive image bytes
    image_id = self.request.get('id', '' )

    image = Image.get_by_id(image_id)

    imgur_link = ''
    if image.imgur_id == 'none':
      imgur_link = meme_default_links[image.type]
    else:
      imgur_link = 'http://i.imgur.com/' + Image.get_imgur_id(image_id)

    params = {
      'title': meme_names[image.type],
      'image_url': imgur_link,
    }

    template = open('static/html/image.html').read()

    self.response.out.write(template % params)

  def post(self):
    # receive image bytes
    image_id = self.request.get('id', '' )
    meme_type = self.request.get('meme_type', '')

    image = Image(
      id=image_id,
      type = meme_type,
    )

    image.put()

    self.response.out.write('success')

