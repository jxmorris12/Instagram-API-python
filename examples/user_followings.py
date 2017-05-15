from InstagramAPI import InstagramAPI
import time
from datetime import datetime

username = ''
pwd = ''
user_id  = ''

API = InstagramAPI(username,pwd)
API.login()

API.getUsernameInfo(user_id)
API.LastJson
following   = []
next_max_id = True
while next_max_id:
    print next_max_id
    #first iteration hack
    if next_max_id == True: next_max_id=''
    _ = API.getUserFollowings(user_id,maxid=next_max_id)
    following.extend ( API.LastJson.get('users',[]))
    next_max_id = API.LastJson.get('next_max_id','')

len(following)
unique_following = {
    f['pk'] : f
    for f in following
}
len(unique_following)
