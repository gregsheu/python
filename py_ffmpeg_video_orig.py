import requests
import ffmpeg
import os
import json
from PIL import Image
from requests.auth import HTTPDigestAuth
import boto3

img = Image.new('RGB', (1920, 1080), (255, 255, 255))
img.save('blank.jpg', 'JPEG')
in1 = None
in2 = None
in3 = None
in4 = None
trailers_ip = {
    'EE37': {'ip': '166.144.184.167'},
    '1D7B': {'ip': '63.46.145.10'},
    '6D2E': {'ip': '166.140.109.245'},
    '839C': {'ip': '166.255.174.128'},
    '2F54': {'ip': '166.161.172.218'},
    'C7A2': {'ip': '166.144.103.113'},
    'FF05': {'ip': '166.253.5.86'},
    '4B71': {'ip': '166.255.58.104'},
    '0B94': {'ip': '166.144.184.116'},
    'A179': {'ip': '166.144.52.59'},
    '8898': {'ip': '166.148.119.237'}
    }
for k,v in trailers_ip.items():
    for i in range(1, 5):
        try:
            r1 = ffmpeg.input('rtsp://admin:admin12345@' + str(v['ip']) + ':554/cam/realmonitor?channel=%s&subtype=0' % i, rtsp_transport = 'tcp')
            (
                ffmpeg
                #.output(r1, '/tmp/'+j['id']+'-%s.mp4' % i, ss=0, t=10)
                .output(r1, k+'-%s.mp4' % i, ss=0, t=10)
                .overwrite_output()
                .run()
            )
            print('Uploading to ksdevbatcheast2')
            s3_c = boto3.client('s3', region_name='us-east-2')
            s3_c.upload_file(k+'-%s.mp4' % i, 'ksdevbatcheast2', k+'-%s.mp4' % i)
            print('Uploaded')
        except:
            print('error on %s cam' % i)
