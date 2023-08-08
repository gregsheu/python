#import cv2

#vcap = cv2.VideoCapture("rtsp://admin:admin12345@166.144.103.115:554/cam/realmonitor?channel=2&subtype=0")
#while(1):
#    ret, frame = vcap.read()
#    cv2.imshow('channel2', frame)
#    cv2.waitKey(1)
import cv2
import time
#import numpy as np

# Create a VideoCapture object
cap = cv2.VideoCapture("rtsp://admin:admin12345@192.168.1.40:554/cam/realmonitor?channel=1&subtype=0")
#cap = cv2.VideoCapture()

# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
#out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
out = cv2.VideoWriter('outpy.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 20, (frame_width,frame_height))

cur_time = time.time()
eventstart = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time))
eventend = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time+30))
while eventstart < eventend:
    cur_time = time.time()
    eventstart = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time))
    ret, frame = cap.read()

    if ret == True: 
      
      # Write the frame into the file 'output.avi'
      out.write(frame)

      # Display the resulting frame    
      #cv2.imshow('frame',frame)

      # Press Q on keyboard to stop recording
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Break the loop
    else:
      break  

# When everything done, release the video capture and video write objects
#cap.release()
#out.release()

# Closes all the frames
#cv2.destroyAllWindows() 
