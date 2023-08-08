import os
import json
import requests
import sys
import time
from requests.auth import HTTPDigestAuth
import urllib

def ptz_control(ip, channel, user, password, mode, direction):
    payload = {'channel': channel}
    param = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
    ptz_url = 'http://%s/cgi-bin/ptz.cgi?action=%s&channel=%s&code=%s&arg1=0&arg2=4&arg3=0&arg4=0' % (ip, mode, channel, direction)
    ptz_resp = requests.get(ptz_url, params=param, auth=HTTPDigestAuth(user, password), stream=False)
    print(ptz_resp.text)

#def ptz_control():
#    #user = 'admin'
#    #password = 'admin12345'
#    #channel = 1
#    #ip = '166.203.161.85'
#    #payload = {'channel': channel}
#    #param = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
#    #mode = 'stop'
#    #direction = 'Right'
#    #ptz_url = 'http://%s/cgi-bin/ptz.cgi?action=%s&channel=%s&code=%s&arg1=0&arg2=4&arg3=0&arg4=0' % (ip, mode, channel, direction)
#    #ptz_resp = requests.get(ptz_url, params=param, auth=HTTPDigestAuth(user, password), stream=False)
#    user = 'admin'
#    password = 'admin12345'
#    channel = 1
#    ip = '166.203.161.85'
#    mode = 'stop'
#    direction = 'Right'
#    payload = {'action': mode, 'channel': channel, 'code': direction, 'arg1': '0', 'arg2': '8', 'arg3': '0', 'arg4': '0'}
#    param = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
#    ptz_url = 'http://%s/cgi-bin/ptz.cgi?' % ip
#    ptz_resp = requests.get(ptz_url, params=param, auth=HTTPDigestAuth(user, password), stream=False)

def main():
    ip = '166.203.161.85'
    channel = 1
    user = 'admin'
    password = 'admin12345'
    ptz_control(ip, channel, user, password, 'start', 'Up')
    ptz_control(ip, channel, user, password, 'start', 'Down')
    time.sleep(2)
    ptz_control(ip, channel, user, password, 'stop', 'Down')
    time.sleep(2)
    ptz_control(ip, channel, user, password, 'start', 'Up')
    time.sleep(2)
    ptz_control(ip, channel, user, password, 'stop', 'Up')
    time.sleep(2)
    ptz_control(ip, channel, user, password, 'start', 'Right')
    time.sleep(2)
    ptz_control(ip, channel, user, password, 'stop', 'Right')
    time.sleep(2)
    ptz_control(ip, channel, user, password, 'start', 'Left')
    time.sleep(2)
    ptz_control(ip, channel, user, password, 'stop', 'Left')
    time.sleep(2)
    ptz_control(ip, channel, user, password, 'start', 'ZoomTele')
    time.sleep(2)
    ptz_control(ip, channel, user, password, 'stop', 'ZoomTele')
    time.sleep(2)
    ptz_control(ip, channel, user, password, 'start', 'ZoomWide')
    time.sleep(2)
    ptz_control(ip, channel, user, password, 'stop', 'ZoomWide')
    time.sleep(2)

if __name__ == '__main__':
    main()
