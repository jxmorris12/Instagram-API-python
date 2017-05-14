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


API.getLikedMedia("")
print API.LastJson
#
# @TODO: Filter out everyone with fewer than 50 or more than 1,000 followers
#

#
# For each image that someone I'm following has posted, download
# >>> Image post date/time
# >>> Number of likes
# and save alongside the username ((just in case))
#


