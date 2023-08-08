import numpy as np
import cv2
import os
import sys
import ffmpeg
import time
import subprocess as sp

#Change NVR encoding to 1280x720 15FPS 1024k; 704x480 15FPS 256k, r=15, g=3 to have lowest latency
#With FRATE=8192k BRATE=16384k FSIZE=1280 to have STREAM=0 r=5, g=1 best resolution and low latency
#With FRATE=4096k BRATE=8192k FSIZE=640 to have STREAM=1 r=5, g=1 best resolution and low latency
def getModel():

    yoloLabels  = 'yolov3/coco.names'
    yoloConfig  = 'yolov3/yolov3.cfg'
    yoloWeights = 'yolov3/yolov3.weights'

    labelsPath  = os.path.join(os.getcwd(), yoloLabels)
    labels      = open(labelsPath).read().strip().split("\n")
    np.random.seed(42)
    colors      = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")

    configPath  = os.path.join(os.getcwd(), yoloConfig)
    weightsPath = os.path.join(os.getcwd(), yoloWeights)

    net         = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    ln          = net.getLayerNames()
    #print(type(ln))
    #print(len(ln))
    #print(ln)
    #ln          = [ln[i[0]-1] for i in net.getUnconnectedOutLayers()]
    ln          = [ln[i-1] for i in net.getUnconnectedOutLayers()]
    #for i in net.getUnconnectedOutLayers():
    #    print(i)
    #    print(ln[i-1])
    #print(labels)
    return(net, ln, labels, colors)

#To use webcam
#command = ['ffmpeg',
#           '-y',
#           '-f', 'rawvideo',
#           '-s', "{}x{}".format(640, 480),
#           '-re',
#           '-vcodec', 'rawvideo',
#           '-pix_fmt', 'bgr24',
#           '-r', '30',
#           '-i', '-',
#           '-c:v', 'libx264',
#           '-vb', '2048k',
#           '-maxrate', '2048k',
#           '-bufsize', '2048k',
#           '-r', '25',
#           '-g', '50',
#           '-tune', 'zerolatency',
#           '-s', "{}x{}".format(640, 480),
#           '-pix_fmt', 'yuv420p',
#           '-preset', 'ultrafast',
#           '-f', 'flv',
#           'rtmp://192.168.1.160/live/cam1']

#IP cam substream
command = ['ffmpeg',
           '-y',
           '-f', 'rawvideo',
           '-s', "{}x{}".format(704, 480),
           '-re',
           '-vcodec', 'rawvideo',
           '-pix_fmt', 'bgr24',
           '-r', '5',
           '-i', '-',
           '-c:v', 'libx264',
           '-vb', '512k',
           '-maxrate', '512k',
           '-bufsize', '2048k',
           '-r', '3',
           '-g', '9',
           '-tune', 'zerolatency',
           '-s', "{}x{}".format(704, 480),
           '-pix_fmt', 'yuv420p',
           '-preset', 'ultrafast',
           '-f', 'flv',
           'rtmp://192.168.1.160/live/cam1']

proc = sp.Popen(command, stdin=sp.PIPE, shell=False)
#To use webcam
#vcap = cv2.VideoCapture(0)
vcap = cv2.VideoCapture("rtsp://admin:admin12345@192.168.1.43:554/cam/realmonitor?channel=1&subtype=1")
#vcap = cv2.VideoCapture("rtsp://admin:admin123456@107.126.218.186:554/cam/realmonitor?channel=1&subtype=1")
yoloConfidence  = 0.5
yoloThreshold   = 0.4

net, ln, labels, colors = getModel()

#cam     = cv2.VideoCapture(0)
#cam     = cv2.VideoCapture('/home/greg/dahuaapi/2021-12-031900-4-1.mp4')
#cam     = cv2.VideoCapture('./2021-12-182147-2_20211218214659_20211218215159.avi')
#cam = cv2.VideoCapture("rtsp://admin:admin12345@192.168.1.43:554/cam/realmonitor?channel=1&subtype=0")
#width  = cam.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
#height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
# or
width  = int(vcap.get(3))  # float `width`
height = int(vcap.get(4))  # float `height`
fps = vcap.get(cv2.CAP_PROP_FPS)
fps = int(vcap.get(5))
print('W ' + str(width) + ' H ' + str(height) + ' FPS ' + str(fps))
#out = cv2.VideoWriter('oakland-3.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (width, height))
#cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
#cv2.resizeWindow("Video", (600, 450))
(W, H) = (None, None)

while vcap.isOpened():

    ret, frame = vcap.read()

    if not ret:
        break
    key = cv2.waitKey(5)

    if (key % 256 == 27):
        print ("End program ...")
        break

    if W is None or H is None:
        (H, W) = frame.shape[:2]

    #Commented out for video files
    #To use webcam that needs flip
    #frame = cv2.flip(frame,1)
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)

    boxes = []
    confidences = []
    classIDs = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > yoloConfidence:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, yoloConfidence, yoloThreshold)

    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            color = [int(c) for c in colors[classIDs[i]]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(labels[classIDs[i]], confidences[i])
            cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    #cv2.putText(frame, "press key 'q' to leave", (410,470), cv2.FONT_HERSHEY_PLAIN, 1.2, (180, 180, 180), 1, cv2.LINE_AA)
    #print(type(frame))
    #cv2.imshow("Video", frame)
    #cv2.waitKey(5)
    if key == ord('q'):
        sys.exit()
    #vcap.release()
    #cv2.destroyAllWindows()
    if not ret:
        print("frame read failed")
        break
    #To use webcam
    #cv2.imshow("Video", frame)
    # YOUR CODE FOR PROCESSING FRAME HERE
    # write to pipe
    #print(frame.tobytes())
    proc.stdin.write(frame.tobytes())
    #cv2.imshow('Live Streaming', frame)
    #cv2.waitKey(1)
