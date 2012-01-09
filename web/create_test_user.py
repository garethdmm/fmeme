from django.utils import simplejson as json
import urllib, urllib2
import random

""" make five test users, and make them all friends """

make_user_url = 'https://graph.facebook.com/271791476212242/accounts/test-users?installed=true&method=post&access_token=271791476212242|NG4tUL8Z4uozz_qvR91_Bo0nCS4&name=effmeme%20'

def main():
  # create five test users
  users = []
  for i in range(0,5):
    users.append(make_user())

  for i in range(0,5):
    for j in range(i+1, 5):
      make_friends(users[i], users[j])

  for i in range(0,5):
    print 'ID: ' + users[i]['id']
    print '\tLogin URL: ' + users[i]['login_url']
    print '\tPassword: ' + users[i]['password']

def make_user():
  url = make_user_url + random.choice(['parker', 'cooper', 'of%20nazareth'])
  print url

  response = urllib2.urlopen(url)

  user = json.loads(response.read())
  print user['login_url']

  return user

def make_friends(user1, user2):
  friend_request(user1, user2)
  accept_request(user1, user2)


def friend_request(user1, user2):
  url = 'https://graph.facebook.com/%s/friends/%s?method=post&access_token=%s' % (user1['id'], user2['id'], user1['access_token'])
  #print url 
  response = urllib2.urlopen(url)
  print 'Request response' + response.read()


def accept_request(user1, user2):
  url = 'https://graph.facebook.com/%s/friends/%s?method=post&access_token=%s' % (user2['id'], user1['id'], user2['access_token'])
  #print url
  response = urllib2.urlopen(url)
  print 'Accept response' + response.read()


if __name__ == '__main__':
  main()
