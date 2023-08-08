import requests
import urllib
import ffmpeg
import time
import threading
import os
import boto3
import json
from requests.auth import HTTPDigestAuth

def main():
    #cam1_ip = os.getenv('CAM1')
    #url = 'http://%s/cgi-bin/eventManager.cgi?action=attach&codes=[CrossLineDetection]' % cam1_ip
    #url = 'http://admin:Admin12345@192.168.1.10/dtect'
    url = 'http://192.168.1.10/dtect/digital_outputs'
    user = 'admin'
    password = 'Admin12345'
    while True:
        resp = requests.get(url, auth=HTTPDigestAuth(user, password))
        print(resp.json())
        events = resp.json()
        print(events)
        if resp.encoding is None:
            resp.encoding = 'utf-8'
        time.sleep(5)

if __name__ == '__main__':
    main()
