import requests
import ffmpeg
import os
from PIL import Image
from requests.auth import HTTPDigestAuth
img = Image.new('RGB', (1920, 1080), (255, 255, 255))
img.save('blank.jpg', 'JPEG')
in1 = None
in2 = None
in3 = None
in4 = None
trailers_ip = {
    'D2B4': {'ip': '166.161.132.132'}
    }
for k,v in trailers_ip.items():
    for i in range(1, 5):
        try:
            r1 = ffmpeg.input('rtsp://admin:admin12345@' + str(v['ip']) + ':554/cam/realmonitor?channel=%s&subtype=0' % i, rtsp_transport = 'tcp')
            (
                ffmpeg
                .output(r1, k + '-%s.jpg' % i, vframes=1)
                .overwrite_output()
                .run()
            )
            in1 = ffmpeg.input(k + '-1.jpg')
            in2 = ffmpeg.input(k + '-2.jpg')
            in3 = ffmpeg.input(k + '-3.jpg')
            #in4 = ffmpeg.input(k + '-4.jpg')
            in4 = ffmpeg.input('blank.jpg')
            in5 = ffmpeg.input(k + '-t1.jpg')
            in6 = ffmpeg.input(k + '-t2.jpg')
        except:
            print('error on %s cam' % i)

(
    ffmpeg
    .concat(
        in1.filter('scale', '800', '450'),
        in2.filter('scale', '800', '450'),
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
        in3.filter('scale', '800', '450'),
        in4.filter('scale', '800', '450'),
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
    .output('marijuana_farm.jpg')
    .overwrite_output()
    .run()
)
