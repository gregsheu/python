import requests
import urllib
import ffmpeg
import os
import time
import threading
from requests.auth import HTTPDigestAuth

def convert_jpgmp4(ip):
    t = 0
    k = 'KingSolarman'
    while t < 6:
        t = t + 1
        for i in range(1, 5):
            try:
                #r1 = ffmpeg.input('rtsp://admin:admin12345@' + str(v['ip']) + ':554/cam/realmonitor?channel=%s&subtype=0' % i, rtsp_transport = 'tcp')
                r1 = ffmpeg.input('rtsp://admin:admin12345@%s:554/cam/realmonitor?channel=%s&subtype=0' % (ip, i), rtsp_transport = 'tcp')
                (
                    ffmpeg
                    .output(r1, k + '%s-%s.jpg' % (t, i), vframes=1)
                    .overwrite_output()
                    .run()
                )
            except:
                print('error on %s cam' % i)
    #for t in range(1, 5):
    for i in range(1, 5):
        (
            ffmpeg.input('./KingSolarman*-%s.jpg' % i, pattern_type='glob', framerate=1)
            #.crop(0, 0, 1280, 720)
            .filter('scale',1280, 720)
            .filter('setsar', sar=1/1)
            .drawtext('King Solarman Inc.', 10, 400, fontcolor='red', fontsize=48, fontfile='/usr/share/fonts/truetype/freefont/FreeSansBold.ttf')
            .output('ks-gif-%s.mp4' % i, t=5, r=29.97)
            .overwrite_output()
            .run()
        )
        v1 = ffmpeg.input('ks-gif-%s.mp4' % i)
        (
            ffmpeg
            .concat(
                v1.setpts('PTS-STARTPTS'),
                #a1.filter('atrim', 45, 55).filter('asetpts', 'PTS-STARTPTS').filter('volume', 0.8),
                v=1,
                a=0,
            )
            .output('KingSolarmanTW-%s.mp4' % i)
            .overwrite_output()
            .run()
        )

def make_tile(ip):
    in1 = None
    in2 = None
    in3 = None
    in4 = None
    k = 'KingSolarmanFront'
    for i in range(1, 5):
        try:
            #r1 = ffmpeg.input('rtsp://admin:admin12345@' + str(v['ip']) + ':554/cam/realmonitor?channel=%s&subtype=0' % i, rtsp_transport = 'tcp')
            r1 = ffmpeg.input('rtsp://admin:admin12345@%s:554/cam/realmonitor?channel=%s&subtype=0' % (ip, i), rtsp_transport = 'tcp')
            (
                ffmpeg
                .output(r1, k + '-%s.jpg' % i, vframes=1)
                .overwrite_output()
                .run()
            )
        except:
            print('error on %s cam' % i)
    in1 = ffmpeg.input(k + '-1.jpg')
    in2 = ffmpeg.input(k + '-2.jpg')
    in3 = ffmpeg.input(k + '-3.jpg')
    in4 = ffmpeg.input(k + '-4.jpg')
    in5 = ffmpeg.input(k + '-t1.jpg')
    in6 = ffmpeg.input(k + '-t2.jpg')
    (
        ffmpeg
        .concat(
            in1.filter('scale', '1280', '720'),
            in2.filter('scale', '1280', '720'),
            )
        .filter('tile', '1x2')
        .filter('setsar', '16', '9')
        .output(k + '-t1.jpg')
        .overwrite_output()
        .run()
    )
    (
        ffmpeg
        .concat(
            in3.filter('scale', '1280', '720'),
            in4.filter('scale', '1280', '720'),
            )
        .filter('tile', '1x2')
        .filter('setsar', '16', '9')
        .output(k + '-t2.jpg')
        .overwrite_output()
        .run()
    )
    (
        ffmpeg
        .concat(
            in5,
            in6,
            )
        .filter('tile', '2x1')
        .filter('setsar', '16', '9')
        .output(k + '-tile.jpg')
        .overwrite_output()
        .run()
    )

def convert_dav(ip, i, eventstart, eventend):
    newtime = eventstart.replace(' ', '')
    newtime = newtime.replace(':', '')
    payload = {'action': 'startLoad', 'channel': i, 'startTime': eventstart, 'endTime': eventend, 'subtype': '0'}
    param = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
    video_url = 'http://%s/cgi-bin/loadfile.cgi?' % ip
    user = 'admin'
    password = 'admin12345'
    video_resp = requests.get(video_url, params=param, auth=HTTPDigestAuth(user, password), stream=True)
    with open('tripvideo-%s-%s.dav' % (i, newtime), 'wb') as f:
        f.write(video_resp.content)
    tripvideo = 'tripvideo-%s-%s.dav' % (i, newtime)
    r = ffmpeg.input(tripvideo)
    (
        ffmpeg
        .output(r, tripvideo[0:-4]+'.mp4', format='mp4')
        .overwrite_output()
        .run()
    )

def main():
    ip = '166.149.88.121'
    #ip = '192.168.1.109'
    #make_tile(ip)
    #convert_jpgmp4(ip)
    t = 0
    cur_time = time.time()
    eventstart = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time-2))
    eventend = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time+5))
    curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time))
    print(curtime)
    print(eventstart)
    print(eventend)
    time.sleep(11)
    convert_dav(ip, 1, eventstart, eventend)
    convert_dav(ip, 2, eventstart, eventend)
    convert_dav(ip, 3, eventstart, eventend)
    convert_dav(ip, 4, eventstart, eventend)

    #t1 = threading.Thread(target=get_con_dav, args=(ip, 1, eventstart, eventend,))
    #t1.start()

if __name__ == '__main__':
    main()
