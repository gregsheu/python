import requests
import urllib
import ffmpeg
import time
import threading
import os
import boto3
from requests.auth import HTTPDigestAuth

def convert_dav(davfile):
    r = ffmpeg.input(davfile)
    (
        ffmpeg
        .output(r, davfile[0:-4]+'.mp4', format='mp4')
        .overwrite_output()
        .run()
    )

def upload_s3(filename):
    time.sleep(5)
    s3_c = boto3.client('s3', region_name='us-west-2')
    s3_c.upload_file('/tmp/'+filename, 'ksdeveventswest2', filename)
    s3_c.put_object_acl(Bucket='ksdeveventswest2', Key=filename, ACL='public-read')

def send_sms(filename):
    s3_url = 'https://ksdeveventswest2.s3-us-west-2.amazonaws.com/'
    topicarn = 'arn:aws:sns:us-west-2:141056581104:ksdevevents'
    sns_c = boto3.client('sns', region_name='us-west-2')
    sns_resp = sns_c.publish(TopicArn=topicarn, Message='Ontario Tripwire Alert!! Link %s%s' % (s3_url, filename))

def get_snap(channel, eventstart, user, password):
    print('Snapshotting')
    payload = {'channel': channel}
    param = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
    snap_url = 'http://192.168.1.102/cgi-bin/snapshot.cgi?'
    snap_resp = requests.get(snap_url, params=param, auth=HTTPDigestAuth(user, password), stream=True)
    newtime = eventstart.replace(' ', '')
    newtime = newtime.replace(':', '')
    filename = 'tripsnap-%s-%s.jpg' % (channel, newtime)
    with open('/tmp/tripsnap-%s-%s.jpg' % (channel, newtime), 'wb') as f:
        f.write(snap_resp.content)
    upload_s3(filename)
    send_sms(filename)
    return 'tripsnap-%s-%s.jpg' % (channel, newtime)

def get_video(channel, eventstart, eventend):
    time.sleep(30)
    print('Videotapping')
    newtime = eventstart.replace(' ', '')
    newtime = newtime.replace(':', '')
    filename = 'tripvideo-%s-%s.mp4' % (channel, newtime)
    payload = {'action': 'startLoad', 'channel': channel, 'startTime': eventstart, 'endTime': eventend, 'subtype': '0'}
    param = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
    print(param)
    video_url = 'http://admin:admin12345@192.168.1.102/cgi-bin/loadfile.cgi?'
    r = ffmpeg.input('%s%s' % (video_url, param))
    (
        ffmpeg
        .output(r, '/tmp/tripvideo-%s-%s.mp4' % (channel, newtime))
        .overwrite_output()
        .run()
    )
    upload_s3(filename)
    send_sms(filename)
    return 'tripvideo-%s-%s.mp4' % (channel, newtime)

def main():
    cam1_ip = os.getenv('CAM1')
    url = 'http://%s/cgi-bin/eventManager.cgi?action=attach&codes=[CrossLineDetection]' % cam1_ip
    user = 'admin'
    password = 'admin12345'
    with requests.get(url, auth=HTTPDigestAuth(user, password), stream=True) as resp:
        if resp.encoding is None:
            resp.encoding = 'utf-8'
        for line in resp.iter_lines():
            decoded_line = line.decode('utf-8')
            print(decoded_line)
            if 'Appear' in decoded_line:
                cur_time = time.time()
                eventstart = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time))
                eventend = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time+30))
                for i in range(1, 3):
                    t1 = threading.Thread(target=get_snap, args=(i, eventstart, user, password,))
                    t1.daemon = False
                    t1.start()
                    t2 = threading.Thread(target=get_video, args=(i, eventstart, eventend,))
                    t2.daemon = False
                    t2.start()

if __name__ == '__main__':
    main()
