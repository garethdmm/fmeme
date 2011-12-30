from google.appengine.ext import webapp
from google.appengine.api import urlfetch

from django.utils import simplejson as json
import logging
import urllib
import base64

from constants import app_id, canvas_page, auth_url

class HomeHandler(webapp.RequestHandler):
  def get(self):
    code = self.request.get('code', '')
    post_id = self.request.get('post_id')

    if post_id != '':
      # we've just made a post, redirect to it, or something like that
      fb_user_id = post_id[ : post_id.find('_')]
      fb_post_id =  post_id[ post_id.find('_') + 1 : ]

      redirect_url = 'https://www.facebook.com/' + fb_user_id + '/posts/' + fb_post_id

      self.redirect(redirect_url)
    elif code != '':
      # we've just been authorized, redirect to canvas
      self.redirect('https://apps.facebook.com/effmeme')

  # the main canvas landing page
  def post(self):
    data = self.get_facebook_data()

    if 'user_id' not in data:
      # haven't been authorized yet
      self.response.out.write('<script>top.location.href="' + auth_url + '";</script>')
    else:
      # we're authorized, show the main page
      token = data['oauth_token']
      fbid = data['user_id']

      feed_url = self.feed_dialog_url()
      f = open('static/html/index.html')
      self.response.out.write(f.read() % {'feed_url': feed_url})


  def self.get_facebook_data(self):
    signed_request = self.request.get('signed_request', '')

    encoded_sig = signed_request.split('.')[0]
    payload = signed_request.split('.')[1]
    payload += '=='

    data = json.loads(base64.urlsafe_b64decode(payload.encode('utf-8')))

    return data


"""
      message = 'Yep, I\'m posting funny cat pictures from the terminal, and I\'m doing it a lot'

      # post to wall by feed dialog
      feed_url = self.feed_dialog_url(
        description='Cat not sure which wat to run',
        caption='I like cats',
        picture='http://i.qkme.me/35lm8j.jpg',
        message='Is this getting annoying yet?',
      )

      self.response.out.write('<script>top.location.href="' + feed_url + '"</script>')

      return
      graph_url = 'https://graph.facebook.com/' + fbid + '/feed'

      logging.info('Graph URL: ' + graph_url)

      # post to wall via graph api
      data = urllib.urlencode({
        'picture': 'http://i.imgur.com/iwbpS.gif',
        'message': message,
        'access_token': token,
      })

      response = urlfetch.fetch(
        url=graph_url,
        payload=data,
        method=urlfetch.POST, 
        deadline=60,
      )

      self.response.out.write(response.content)
      logging.info('Final URL: ' + str(response.final_url))
      logging.info('Content: ' + (response.content))

    return 
"""

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
