#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

from InstagramAPI import InstagramAPI
import config

#
# Log in to API
#
API = InstagramAPI(config.user, config.password)
API.login()


user_id = config.user_id

pics = []
next_max_id = True
while next_max_id:
  # first iteration hack
  if next_max_id == True: next_max_id=''
  _ = API.getUserFeed(user_id,maxid=next_max_id)
  pics.extend ( API.LastJson.get('items',[]))
  next_max_id = API.LastJson.get('next_max_id','')


for pic in pics: 
  d = {}
  d['like_count'] = pic.get('like_count')
  d['taken_at']  = pic.get('taken_at')
  d["user_id"] = user_id
  try:
    d['caption'] = pic.get('caption').get('text')
  except AttributeError:
    d['caption'] = ""
  print d
# print map(lambda x: x["text"], pics)
