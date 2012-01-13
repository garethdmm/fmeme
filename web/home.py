from google.appengine.ext import webapp
from google.appengine.api import urlfetch

from django.utils import simplejson as json
import logging
import urllib
import base64

from constants import app_id, canvas_page, auth_url

class HomeHandler(webapp.RequestHandler):
  def get(self):
    feed_url = self.feed_dialog_url()
    f = open('static/html/index.html')
    self.response.out.write(f.read() % {'feed_url': feed_url})
    return

    code = self.request.get('code', '')
    post_id = self.request.get('post_id')

    if post_id != '':
      # facebook redirected to us after posting something
      # bounce the user back to the new post

      fb_user_id = post_id[ : post_id.find('_')]
      fb_post_id =  post_id[ post_id.find('_') + 1 : ]

      redirect_url = 'https://www.facebook.com/' + fb_user_id + '/posts/' + fb_post_id

      self.redirect(redirect_url)
    elif code != '':
      # we've just been authorized by the user
      # redirect to the canvas page

      self.redirect('https://apps.facebook.com/effmeme')

  def post(self):
    data = self.get_facebook_data()

    if False:#'user_id' not in data:
      # haven't been authorized yet
      # bounce the user to the facebook authorization page

      self.response.out.write('<script>top.location.href="' + auth_url + '";</script>')
    else:
      # we've been authorized
      # show the main page

      feed_url = self.feed_dialog_url()
      f = open('static/html/index.html')
      self.response.out.write(f.read() % {'feed_url': feed_url})


  def get_facebook_data(self):
    signed_request = self.request.get('signed_request', '')

    encoded_sig = signed_request.split('.')[0]
    payload = signed_request.split('.')[1]
    payload += '=='

    data = json.loads(base64.urlsafe_b64decode(payload.encode('utf-8')))

    return data


  def feed_dialog_url(self, picture=None, link=None, description=None, caption=None, message=None):
    feed_url = "https://www.facebook.com/dialog/feed?app_id=" + app_id + "&redirect_uri=" + urllib.quote(canvas_page) 

    if picture != None:
      feed_url += '&picture=' + urllib.quote(picture)
    if description != None:
      feed_url += '&description=' + urllib.quote(description)
    if caption != None:
      feed_url += '&caption=' + urllib.quote(caption)
    if message != None:
      feed_url += '&message=' + urllib.quote(message)

    return feed_url
