#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

import csv
import config
import json

from InstagramAPI import InstagramAPI

#
# Log in to API
#
API = InstagramAPI(config.user, config.password)
API.login()


outfile_name = "out-test.csv"
user_id = config.user_id

pics = []
next_max_id = True
while next_max_id:
  # first iteration hack
  if next_max_id == True: next_max_id=''
  _ = API.getUserFeed(user_id,maxid=next_max_id)
  pics.extend ( API.LastJson.get('items',[]))
  next_max_id = API.LastJson.get('next_max_id','')


data = []
# ['taken-at', 'like-count', 'user_id', 'caption']
for pic in pics: 
  a = []
  a.append(pic.get('like_count'))
  a.append(pic.get('taken_at'))
  a.append(user_id)
  try:
    a.append(str( pic.get('caption').get('text') ))
  except AttributeError:
    a.append("")
  data.append(a)

print a

with open(outfile_name, 'wb') as csvfile:
  spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
  spamwriter.writerow(['taken-at', 'like-count', 'user_id', 'caption'])
  for data_row in data:
    spamwriter.writerow(data_row)