import ffmpeg
import time
import datetime
import os
from requests.auth import HTTPDigestAuth
import pickle, os.path, base64, mimetypes, requests, urllib, time, threading, os, json, ffmpeg, logging

def get_snap(ip, channel, eventstart, eventend):
    newtime = eventstart.replace(' ', '')
    newtime = newtime.replace(':', '')
    date_dir = eventstart[0:eventstart.index(' ')]
    if os.path.exists('/tmp/%s' % date_dir):
        pass
    else:
        os.mkdir('/tmp/%s' % date_dir)
        os.chmod('/tmp/%s' % date_dir, 0o1777)
    filename =  'tripsnap-%s-%s.jpg' % (str(channel)+ip.split('.')[-1], newtime)
    payload = {'action': 'startLoad', 'channel': channel, 'startTime': eventstart, 'endTime': eventend, 'subtype': '0'}
    param = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
    video_url = 'http://%s/cgi-bin/loadfile.cgi?' % ip
    user = 'admin'
    password = 'admin12345'
    eventstart = eventstart.replace(' ', '%20')
    eventend = eventend.replace(' ', '%20')
    url =  'http://%s:%s@%s/cgi-bin/loadfile.cgi?action=startLoad&channel=%s&startTime=%s&endTime=%s&subtype=0' % (user, password, ip, channel, eventstart, eventend)
    print(url)
    video_resp = requests.get(video_url, params=param, auth=HTTPDigestAuth(user, password), stream=True)
    r = ffmpeg.input(url)
    (
        ffmpeg
        #.output(r, '/tmp/%s/tripsnap-%s-%s.mp4' % (date_dir, str(channel)+ip.split('.')[-1], newtime), vcodec='libx264', format='mp4')
        .output(r, '/tmp/%s/tripsnap-%s-%s.jpg' % (date_dir, str(channel)+ip.split('.')[-1], newtime), vframes=1)
        .overwrite_output()
        .run()
    )
    return '%s/%s' % (date_dir, filename)

def convert_dav(ip, channel, eventstart, eventend):
    newtime = eventstart.replace(' ', '')
    newtime = newtime.replace(':', '')
    date_dir = eventstart[0:eventstart.index(' ')]
    if os.path.exists('/tmp/%s' % date_dir):
        pass
    else:
        os.mkdir('/tmp/%s' % date_dir)
        os.chmod('/tmp/%s' % date_dir, 0o1777)
    filename =  'tripvideo-%s-%s.mp4' % (str(channel)+ip.split('.')[-1], newtime)
    payload = {'action': 'startLoad', 'channel': channel, 'startTime': eventstart, 'endTime': eventend, 'subtype': '0'}
    param = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
    video_url = 'http://%s/cgi-bin/loadfile.cgi?' % ip
    user = 'admin'
    password = 'admin12345'
    video_resp = requests.get(video_url, params=param, auth=HTTPDigestAuth(user, password), stream=True)
    with open('/tmp/%s/tripvideo-%s-%s.dav' % (date_dir, str(channel)+ip.split('.')[-1], newtime), 'wb') as f:
        f.write(video_resp.content)
    #r = ffmpeg.input('/tmp/%s/tripvideo-%s-%s.dav' % (date_dir, str(channel)+ip.split('.')[-1], newtime))
    #(
    #    ffmpeg
    #    #.output(r, '/tmp/%s/tripvideo-%s-%s.mp4' % (date_dir, str(channel)+ip.split('.')[-1], newtime), vcodec='libx264', format='mp4')
    #    .output(r, '/tmp/%s/tripvideo-%s-%s.jpg' % (date_dir, str(channel)+ip.split('.')[-1], newtime), vframes=1)
    #    .overwrite_output()
    #    .run()
    #)
    #return '%s/%s' % (date_dir, filename)

def pack_jpgs(channel):
    (
        ffmpeg.input('/tmp/2021-07-03/tripsnap-%s*.jpg' % channel, pattern_type='glob', framerate=1)
        #.crop(0, 0, 1280, 720)
        .filter('scale',1280, 680)
        .filter('setsar', sar=1/1)
        .drawtext('Created by G.S. @King Solarman Inc.', 10, 400, fontcolor='red', fontsize=24, fontfile='/usr/share/fonts/truetype/freefont/FreeSansBold.ttf')
        .output('jpgs-%s.mp4' % channel, r=29.97)
        .overwrite_output()
        .run()
    )
    (  
        ffmpeg.input('jpgs-%s.mp4' % channel)
        .setpts('0.054*PTS')
        .output('timelapse-%s.mp4' % channel)
        .overwrite_output()
        .run()
    )

def main():
    #ip = '107.126.216.141'
    ip = '166.255.58.104'
    date_counter = 6
    while date_counter < 7:
        h = 17 
        while h < 24:
            m = 0 
            while m < 60:
                if date_counter < 10:
                    eventstart = datetime.datetime.strptime('2021-07-0%s %s:%s:00' % (date_counter, h, m), '%Y-%m-%d %H:%M:%S')
                    eventend = datetime.datetime.strptime('2021-07-0%s %s:%s:00' % (date_counter, h, m), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(seconds=60) 
                else:
                    eventstart = datetime.datetime.strptime('2021-07-%s %s:%s:00' % (date_counter, h, m), '%Y-%m-%d %H:%M:%S')
                    eventend = datetime.datetime.strptime('2021-07-%s %s:%s:00' % (date_counter, h, m), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(seconds=60) 
                print(eventstart)
                print(eventend)
                #convert_dav(ip, 1, str(eventstart), str(eventend))
                #convert_dav(ip, 2, str(eventstart), str(eventend))
                #convert_dav(ip, 3, str(eventstart), str(eventend))
                #convert_dav(ip, 4, str(eventstart), str(eventend))
                get_snap(ip, 1, str(eventstart), str(eventend))
                get_snap(ip, 2, str(eventstart), str(eventend))
                if h == 18 and m == 41:
                    ...
                else:
                    get_snap(ip, 3, str(eventstart), str(eventend))
                get_snap(ip, 4, str(eventstart), str(eventend))
                m += 1
            h += 1
        #pack_jpgs(1, date_counter)
        #pack_jpgs(2, date_counter)
        #pack_jpgs(3, date_counter)
        #pack_jpgs(4, date_counter)
        date_counter += 1
        #cur_time = time.strptime('2021-06-0%s 12:53:00' % date_counter, '%Y-%m-%d %H:%M:%S')
        #eventstart = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time))
        #eventend = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time+5))
        #eventstart = time.strftime('%Y-%m-%d %H:%M:%S', cur_time)
        #cur_time_5 = datetime.strptime('2021-06-0%s 12:53:00' % date_counter, '%Y-%m-%d %H:%M:%S').timestamp() + 5
        #eventend = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time_5))

if __name__ == '__main__':
    main()
