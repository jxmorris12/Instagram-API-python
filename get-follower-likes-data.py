#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

import config
import csv
from InstagramAPI import InstagramAPI
import random
import time

# unicode helper
def _u(s):
  return s.encode('utf-8').strip()

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
    print next_max_id
    #first iteration hack
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

# (Temporary) trim
followers = followers[:100]

follower_ids = map(lambda x: x["pk"], followers)

print follower_ids

#
# @TODO: Filter out everyone with fewer than 50 or more than 1,000 followers
#

#
# For each image that someone I'm following has posted, download
# >>> Image post date/time
# >>> Number of likes
# >>> caption
# and save alongside the username ((just in case))
#

outfile_name = "out.csv"
#user_id = config.user_id
data = []

i = 1
for user_id in follower_ids:
  print i, "/", len(follower_ids)
  i += 1
  pics = []
  next_max_id = True
  while next_max_id:
    # first iteration hack
    if next_max_id == True: next_max_id=''
    _ = API.getUserFeed(user_id,maxid=next_max_id)
    pics.extend ( API.LastJson.get('items',[]))
    next_max_id = API.LastJson.get('next_max_id','')
    time.sleep(0.25 + random.random() / 4) # slightly throttle requests to Instagram. Just being polite.
  # ['taken-at', 'like-count', 'user_id', 'caption']
  for pic in pics: 
    a = []
    a.append(pic.get('like_count'))
    a.append(pic.get('taken_at'))
    a.append(user_id)
    try:
      a.append(_u(pic.get('caption').get('text')))
    except AttributeError:
      a.append("")
    data.append(a)

#
# Write Data to CSV
#
with open(outfile_name, 'wb') as csvfile:
  spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
  spamwriter.writerow(['taken-at', 'like-count', 'user_id', 'caption'])
  for data_row in data:
    spamwriter.writerow(data_row)


#
# Done
#
print "Written to", outfile_name + "."
