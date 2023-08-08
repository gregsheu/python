import cv2
import ffmpeg
import time

vcap = cv2.VideoCapture("rtsp://admin:admin12345@192.168.1.77:554/cam/realmonitor?channel=1&subtype=0")
while(1):
    ret, frame = vcap.read()
    print(frame.tobytes())
    cv2.imshow('channel2', frame)
    cv2.waitKey(1)
