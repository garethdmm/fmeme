from google.appengine.ext import webapp
from google.appengine.api import urlfetch

from django.utils import simplejson as json

from constants import imgur_upload_url, imgur_key
import urllib
import base64
import logging
import os

class BakeHandler(webapp.RequestHandler):
  def post(self):
    # receive image bytes
    image = self.request.get('image', '' )

    # strip data uri prefix
    image = image[image.find('base64,') + 7 : ]

    # post to imgur to get the url
    data = urllib.urlencode({
      'key': imgur_key,
      'image': image, 
      'type': 'base64',
    })

    response = urlfetch.fetch(
      url=imgur_upload_url,
      payload=data,
      method=urlfetch.POST, 
      deadline=60,
    )

    # parse response
    # TODO error handling
    response_data = json.loads(response.content)
    image_id = response_data['upload']['links']['original']

    image_id = image_id[image_id.rfind('/') + 1 : ]
    image_url = 'http://' + os.environ['HTTP_HOST'] + '/image?id=' + image_id

    # return the imgur url
    self.response.out.write(image_url)

