import numpy as np
import cv2
import os
import sys
import ffmpeg
import time
import subprocess as sp

vcap = cv2.VideoCapture("silverwoodbigstocker.mp4")
width  = int(vcap.get(3))  # float `width`
height = int(vcap.get(4))  # float `height`
fps = int(vcap.get(5))
out = cv2.VideoWriter('silverwoodbig.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (height, width))

while vcap.isOpened():

    ret, frame = vcap.read()
    #cv2.imshow("Video", frame)
    #image = cv2.flip(frame, 0)
    image = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    out.write(image)
    if not ret:
        print("frame read failed")
        break
    #cv2.imshow('Live Streaming', image)
    #cv2.imwrite('flip.jpg', image)
    cv2.waitKey(50000)
