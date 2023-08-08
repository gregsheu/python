from requests.auth import HTTPDigestAuth
import requests

user = 'admin'
password = 'admin12345'
resp = requests.get('http://166.144.103.115/cgi-bin/mjpg/video.cgi?channel=3', auth=HTTPDigestAuth(user, password), stream=True)

for line in resp.iter_lines():
    # filter out keep-alive new lines
    if line:
        print(line)
        #with open('thisfile.mp4', 'wb') as f:
    #f.write(resp.content)
