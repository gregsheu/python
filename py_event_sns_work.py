import requests
import urllib
import ffmpeg
import boto3
import time
import threading
from requests.auth import HTTPDigestAuth

def run_ffmpeg(channel, eventstart, eventend):
    payload = {'action': 'startLoad', 'channel': channel, 'startTime': eventstart, 'endTime': eventend, 'subtype': '0'}
    param = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
    print(param)
    video_url = 'http://admin:admin12345@192.168.1.102/cgi-bin/loadfile.cgi?'
    r = ffmpeg.input('%s%s' % (video_url, param))
    (
        ffmpeg
        .output(r, 'tripvideo-1-%s.mp4' %(eventstart))
        .overwrite_output()
        .run()
    )

def convert_dav(davfile):
    r = ffmpeg.input(davfile)
    (
        ffmpeg
        .output(r, davfile[0:-4]+'.mp4', format='mp4')
        .overwrite_output()
        .run()
    )

sns_c = boto3.client('sns', region_name='us-west-2')
topicarn = 'arn:aws:sns:us-west-2:141056581104:ksdevevents'

url = 'http://192.168.1.102/cgi-bin/eventManager.cgi?action=attach&codes=[CrossLineDetection]'
user = 'admin'
password = 'admin12345'
with requests.get(url, auth=HTTPDigestAuth(user, password), stream=True) as resp:
    if resp.encoding is None:
        resp.encoding = 'utf-8'
    for line in resp.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            print(decoded_line)
            if 'Appear' in decoded_line:
                cur_time = time.time()
                eventstart = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time))
                eventend = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time+30))
                for i in range(1, 3):
                    payload = {'channel': i}
                    param = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
                    snap_url = 'http://192.168.1.102/cgi-bin/snapshot.cgi?'
                    snap_resp = requests.get(snap_url, params=param, auth=HTTPDigestAuth(user, password), stream=True)
                    newtime = eventstart.replace(' ', '')
                    newtime = newtime.replace(':', '')
                    with open('tripsnap-%s-%s.jpg' % (i, newtime), 'wb') as f:
                        f.write(snap_resp.content)
                    time.sleep(1)
                    s3_c = boto3.client('s3', region_name='us-west-2')
                    s3_c.upload_file('tripsnap-%s-%s.jpg' % (i, newtime), 'ksdeveventswest2', 'tripsnap-%s-%s.jpg' % (i, newtime))
                    tripsnapshot = 'tripsnap-%s-%s.jpg' % (i, newtime)
                    s3_c.put_object_acl(Bucket='ksdeveventswest2', Key=tripsnapshot, ACL='public-read')
                    s3_url = 'https://ksdeveventswest2.s3-us-west-2.amazonaws.com/'
                    sns_resp = sns_c.publish(TopicArn=topicarn, Message='Ontario Tripwire Alert!! Picture link %s%s' % (s3_url, tripsnapshot))
                    print('Sending to SNS')
                    payload = {'action': 'startLoad', 'channel': i, 'startTime': eventstart, 'endTime': eventend, 'subtype': '0'}
                    param = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
                    video_url = 'http://192.168.1.102/cgi-bin/loadfile.cgi?'
                    video_resp = requests.get(video_url, params=param, auth=HTTPDigestAuth(user, password), stream=True)
                    with open('tripvideo-%s-%s.dav' % (i, newtime), 'wb') as f:
                        f.write(video_resp.content)
                    tripvideo = 'tripvideo-%s-%s.dav' % (i, newtime)
                    time.sleep(30)
                    t1 = threading.Thread(target=convert_dav, args=(tripvideo,))
                    t1.start()
                    t1.join()
                    t2 = threading.Thread(target=run_ffmpeg, args=(i, eventstart, eventend,))
                    t2.start()
                    t2.join()
                    time.sleep(10)
                    tripvideo = 'tripvideo-%s-%s.mp4' % (i, newtime)
                    s3_c.upload_file('tripvideo-%s-%s.mp4' % (i, newtime), 'ksdeveventswest2', 'tripvideo-%s-%s.mp4' % (i, newtime))
                    s3_c.put_object_acl(Bucket='ksdeveventswest2', Key=tripvideo, ACL='public-read')
                    s3_url = 'https://ksdeveventswest2.s3-us-west-2.amazonaws.com/'
                    sns_resp = sns_c.publish(TopicArn=topicarn, Message='Ontario Tripwire Alert!! Video link %s%s' % (s3_url, tripvideo))
