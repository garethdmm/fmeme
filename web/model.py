from google.appengine.ext import db

import string
import random

class Image(db.Model):
  id = db.StringProperty()
  imgur_id = db.StringProperty(default='none')
  type = db.StringProperty()

  @staticmethod
  def get_by_id(uid):
    return Image.all().filter('id =', uid).get()

  @staticmethod
  def get_imgur_id(uid):
    image = Image.all().filter('id =', uid).get()
    return image.imgur_id

  @staticmethod
  def make_id():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
