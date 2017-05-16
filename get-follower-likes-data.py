#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

import config
import csv
import datetime
import random
import time

from InstagramAPI import InstagramAPI

min_followers = 20
max_followers = 2000
datum_limit = 50


# unicode helper
def _u(s):
  return s.encode('utf-8').strip()

# datetime helper
def _seconds_from_midnight(d):
  t = datetime.datetime.fromtimestamp(int(d))
  return (t.hour * 60 * 60) + (t.minute * 60) + t.second

# sleep to slightly throttle requests to Instagram. Just being polite.
def _wait():
  time.sleep(1.0 + random.random())

#
# Log in to API
#
API = InstagramAPI(config.user, config.password)
API.login()

#
# Get list of everyone I'm following
#
API.getUsernameInfo(config.user_id)
API.LastJson
following   = []
next_max_id = True
while next_max_id:
    if next_max_id == True: next_max_id=''
    _ = API.getUserFollowings(config.user_id,maxid=next_max_id)
    following.extend ( API.LastJson.get('users',[]))
    next_max_id = API.LastJson.get('next_max_id','')

unique_following = {
    f['pk'] : f
    for f in following
}
followers = unique_following.values()
follower_usernames = map(lambda x: x["username"], followers)

# Trim data set to <datum_limit> persons.
followers = followers[:datum_limit]

#
# Filter out everyone with fewer than 50 or more than 1,000 followers
#

print "Checking follower counts."

follower_info = []

i = 1
for follower in followers:
  print "[F]", i, "/", len(followers)
  i += 1
  user_id = follower["pk"]
  _ = API.getUsernameInfo(user_id)
  try:
    num_followers = API.LastJson.get(u'user').get(u'follower_count')
  except AttributeError:
    print API.LastJson
    exit(-1)
  if min_followers <= num_followers and num_followers <= max_followers:
    follower_info.append( (user_id,num_followers) )
  _wait()

#
# For each image that someone I'm following has posted, download
# >>> Image post date/time
# >>> Number of likes
# >>> caption
# and save alongside the username ((just in case)) and follower count.
#

print "Downloading image like data."
outfile_name = "out_" + str(datum_limit) + ".csv"
#user_id = config.user_id
data = []

i = 1
for (user_id, user_followers) in follower_info:
  print "[P]", i, "/", len(follower_info)
  i += 1
  pics = []
  next_max_id = True
  # Gather all media data
  while next_max_id:
    if next_max_id == True: next_max_id=''
    _ = API.getUserFeed(user_id,maxid=next_max_id)
    pics.extend ( API.LastJson.get('items',[]))
    next_max_id = API.LastJson.get('next_max_id','')
    _wait()
  # Iterate through each item of media
  for pic in pics: 
    #
    a = []
    #
    taken_at = pic.get('taken_at')
    a.append(taken_at)
    a.append(_seconds_from_midnight(taken_at))
    #
    a.append(pic.get('like_count'))
    #
    a.append(user_followers)
    a.append(user_id)
    #
    try:
      #
      a.append(_u(pic.get('caption').get('text')))
      #
    except AttributeError:
      #
      a.append("")
      #
    #
    data.append(a)
    #

#
# Write Data to CSV
#
print "Saving data."
with open(outfile_name, 'wb') as csvfile:
  spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
  spamwriter.writerow(['taken-at', 'seconds-from-midnight', 'like-count', 'user_id', 'user-followers', 'caption'])
  for data_row in data:
    spamwriter.writerow(data_row)


#
# Done
#
print "Written to", outfile_name + "."