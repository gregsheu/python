import requests
import urllib
import ffmpeg
import os
import time

#r1 = ffmpeg.input('dahuaapi/2021-12-181025-2.mp4', ss=135)
#(
#    ffmpeg
#    .output(r1, '1025.jpg', vframes=1)
#    .overwrite_output()
#    .run()
#)
r1 = ffmpeg.input('Pictures/10152022/MAH00806.MP4', ss=1000)
(
    ffmpeg
    .output(r1, 'MAH00806-1.jpg', vframes=1)
    .overwrite_output()
    .run()
)
