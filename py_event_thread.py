import requests
import urllib
import ffmpeg
import boto3
import time
import threading
from requests.auth import HTTPDigestAuth

def convert_dav(davfile):
    r = ffmpeg.input(davfile)
    (
        ffmpeg
        .output(r, davfile[0:-4]+'.mp4', format='mp4')
        .overwrite_output()
        .run()
    )

def get_video(channel, eventstart, eventend):
    newtime = eventstart.replace(' ', '')
    newtime = newtime.replace(':', '')
    payload = {'action': 'startLoad', 'channel': channel, 'startTime': eventstart, 'endTime': eventend, 'subtype': '0'}
    param = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
    print(param)
    video_url = 'http://admin:admin12345@192.168.1.102/cgi-bin/loadfile.cgi?'
    r = ffmpeg.input('%s%s' % (video_url, param))
    (
        ffmpeg
        .output(r, 'tripvideo-%s-%s.mp4' % (channel, newtime))
        .overwrite_output()
        .run()
    )
    return 'tripvideo-%s-%s.mp4' % (channel, newtime)

def get_snap(channel, eventstart, user, password):
    payload = {'channel': channel}
    param = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
    snap_url = 'http://192.168.1.102/cgi-bin/snapshot.cgi?'
    snap_resp = requests.get(snap_url, params=param, auth=HTTPDigestAuth(user, password), stream=True)
    newtime = eventstart.replace(' ', '')
    newtime = newtime.replace(':', '')
    with open('tripsnap-%s-%s.jpg' % (channel, newtime), 'wb') as f:
        f.write(snap_resp.content)
    return 'tripsnap-%s-%s.jpg' % (channel, newtime)

def upload_s3(eventstart, filename):
    newtime = eventstart.replace(' ', '')
    newtime = newtime.replace(':', '')
    s3_c = boto3.client('s3', region_name='us-west-2')
    s3_c.upload_file(filename, 'ksdevbatchwest2', filename)
    s3_c.put_object_acl(Bucket='ksdevbatchwest2', Key=filename, ACL='public-read')

def send_sms(filename):
    s3_url = 'https://ksdevbatchwest2.s3-us-west-2.amazonaws.com/'
    topicarn = 'arn:aws:sns:us-west-2:141056581104:ksdevtesttripwire'
    sns_c = boto3.client('sns', region_name='us-west-2')
    sns_resp = sns_c.publish(TopicArn=topicarn, Message='Ontario Tripwire Alert!! Link %s%s' % (s3_url, filename))

def event_queue(eventstart):
    l = []
    l.append(eventstart)
    return l

def main():
    eventstart = '2021-01-22'
    t1 = threading.Thread(target=event_queue, args=(eventstart,))
    t1.start()

#def main():
#    url = 'http://192.168.1.102/cgi-bin/eventManager.cgi?action=attach&codes=[CrossLineDetection]'
#    user = 'admin'
#    password = 'admin12345'
#    with requests.get(url, auth=HTTPDigestAuth(user, password), stream=True) as resp:
#        if resp.encoding is None:
#            resp.encoding = 'utf-8'
#        for line in resp.iter_lines():
#            decoded_line = line.decode('utf-8')
#            print(decoded_line)
#            if 'Appear' in decoded_line:
#                cur_time = time.time()
#                eventstart = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time))
#                eventend = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time+30))
#                for i in range(1, 3):
#                    filename = get_snap(i, eventstart, user, password)
#                    upload_s3(eventstart, filename)
#                    send_sms(filename)
#                    time.sleep(30)
#                    t1 = threading.Thread(target=get_video, args=(i, eventstart, eventend,))
#                    t1.start()
#                    t1.join()
#                    filename = filename.replace('snap', 'video')
#                    filename = filename.replace('jpg', 'mp4')
#                    upload_s3(eventstart, filename)
#                    send_sms(filename)
 
if __name__ == '__main__':
    main()
