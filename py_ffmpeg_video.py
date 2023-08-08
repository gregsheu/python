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
s3_c = boto3.client('s3', region_name='us-east-2')
resp = s3_c.get_object(Bucket='ksdevbatcheast2', Key='data.json')
data_json = json.load(resp['Body'])
for j in data_json:
    for i in range(1, 5):
        try:
            r1 = ffmpeg.input('rtsp://admin:admin12345@' + str(j['ip']) + ':554/cam/realmonitor?channel=%s&subtype=0' % i, rtsp_transport = 'tcp')
            (
                ffmpeg
                .output(r1, j['id'] + '-%s.mp4' % i, ss=0, t=10)
                .overwrite_output()
                .run()
            )
            print('Uploading to ksdevbatcheast2')
            s3_c = boto3.client('s3', region_name='us-east-2')
            s3_c.upload_file(j['id'] + '-%s.mp4' % i, 'ksdevbatcheast2', j['id'] + '-%s.mp4' % i)
            print('Uploaded')
        except:
            print('error on %s cam' % i)
