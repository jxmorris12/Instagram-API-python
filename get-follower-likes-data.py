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
followers = followers[:5]

print followers 

#
# @TODO: Filter out everyone with fewer than 50 or more than 1,000 followers
#

#
# For each image that someone I'm following has posted, download
# >>> Image post date/time
# >>> Number of likes
# and save alongside the username ((just in case))
#


