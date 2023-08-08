from requests.auth import HTTPDigestAuth
import requests
import json
import time
import urllib

user = 'admin'
password = 'admin12345'

cur_time = time.time()
eventtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time))
eventendtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time+30))
print(eventtime)
print(eventendtime)
time.sleep(60)
payload = {'action': 'startLoad', 'channel': '1', 'startTime': eventtime, 'endTime': eventendtime, 'subtype': '0'}
#urllib.quote_plus = urllib.quote
param = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
video_url = 'http://192.168.1.102/cgi-bin/loadfile.cgi?'
print(video_url + param)
video_resp = requests.get(video_url, params=param, auth=HTTPDigestAuth(user, password), stream=True)
with open('tripvideo.dav', 'wb') as f:
    f.write(video_resp.content)
