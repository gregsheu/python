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
try:
    #r1 = ffmpeg.input('rtsp://admin:admin12345@166.167.6.47:554/cam/realmonitor?channel=3&subtype=0', rtsp_transport = 'tcp')
    r1 = ffmpeg.input('rtsp://admin:admin12345@192.168.1.102:554/cam/realmonitor?channel=1&subtype=0', rtsp_transport = 'tcp')
    #r1 = ffmpeg.input('http://admin:admin12345@192.168.1.102/cgi-bin/loadfile.cgi?action=startLoad&channel=2&startTime=2021-01-29%2017:32:38&endTime=2021-01-29%2017:33:08&subtype=0')
    #r1 = ffmpeg.input('http://admin:admin12345@166.167.6.47/cgi-bin/loadfile.cgi?action=startLoad&channel=3&startTime=2020-12-15%2002:51:45&endTime=2020-12-15%2002:53:45&subtype=0') 
    ( 
        ffmpeg
        #.output(r1, '910C-3.mp4', ss=0, t=10)
        #.output(r1, '102.mp4', r=1, vb='512k', vcodec='libx264', maxrate='512k', bufsize='1024k', g=2, pix_fmt='yuvj420p')
        .output(r1, '102.mp4', ss=0, t=30, vsync='passthrough')
        #.output(r1, '109-p.mp4', ss=0, t=30, vsync='passthrough')
        #.output(r1, '109-p1.mp4', ss=0, t=30)
        .overwrite_output()
        .run()
    )
except:
    print('error on cam')
