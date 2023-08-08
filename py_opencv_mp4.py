import cv2
import ffmpeg
import time
from io import BytesIO
import numpy as np

# Create a VideoCapture object
#cap = cv2.VideoCapture("chevvy.yuv")
#cap = cv2.VideoCapture("rtsp://admin:admin12345@192.168.1.43:554/cam/realmonitor?channel=1&subtype=0")
cap = cv2.VideoCapture(0)
width = int(cap.get(3))
height = int(cap.get(4))
fps = int(cap.get(5))
out = cv2.VideoWriter('cam.mp4', cv2.VideoWriter_fourcc('m','p','4', 'v'), fps, (width, height))
while True:
    ret, frame = cap.read()
    #print(frame.shape)
    #print(frame.ndim)
    #print(frame[0])
    #cv2.imshow('Video', frame)
    out.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
       break

cap.release()
out.release()
cv2.destroyAllWindows() 
