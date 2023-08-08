import cv2
import ffmpeg
import time
from io import BytesIO

cap = cv2.VideoCapture("rtsp://admin:admin12345@192.168.1.43:554/cam/realmonitor?channel=1&subtype=0")
width = int(cap.get(3))
height = int(cap.get(4))
fps = int(cap.get(5))
out1 = cv2.VideoWriter('out1.avi',cv2.VideoWriter_fourcc('M','J','P','G'), fps, (width, height))
out2 = cv2.VideoWriter('out2.mp4',cv2.VideoWriter_fourcc('m','p','4', 'v'), fps, (width, height))
while(1):
    ret, frame = cap.read()
    out1.write(frame)
    out2.write(frame)
    success, encoded_image = cv2.imencode('.jpg', frame)
    frames = cv2.resize(frame, (1920, 1080))
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]
    cv2.imwrite('cvwrite.jpg', frames)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
cap.release()
out1.release()
out2.release()
cv2.destroyAllWindows() 
