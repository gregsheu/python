import numpy as np
import cv2
import os
import sys
import ffmpeg
import time
import datetime
import glob

def jpg2mp4(date_dir):
    for f in glob.glob('snap/%s/*.jpg' % date_dir):
        b = os.path.getsize(f)
        if b == 0:
            os.remove(f)
    (
        ffmpeg.input('snap/%s/img*.jpg' % date_dir, pattern_type='glob', framerate=1)
        .output('snap/%s/%s-tesla1.mp4' % (date_dir, date_dir), r=3)
        .overwrite_output()
        .run()
    )
    #(
    #    ffmpeg.input('snap/%s/tripsnap-2*.jpg' % date_dir, pattern_type='glob', framerate=1)
    #    .output('snap/%s/%s-tesla2.mp4' % (date_dir, date_dir), r=3)
    #    .overwrite_output()
    #    .run()
    #)
    #(
    #    ffmpeg.input('snap/%s/tripsnap-3*.jpg' % date_dir, pattern_type='glob', framerate=1)
    #    .output('snap/%s/%s-tesla3.mp4' % (date_dir, date_dir), r=3)
    #    .overwrite_output()
    #    .run()
    #)
    #(
    #    ffmpeg.input('snap/%s/tripsnap-4*.jpg' % date_dir, pattern_type='glob', framerate=1)
    #    .output('snap/%s/%s-tesla4.mp4' % (date_dir, date_dir), r=3)
    #    .overwrite_output()
    #    .run()
    #)

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

def detect_video(date_dir):
    yoloConfidence  = 0.5
    yoloThreshold   = 0.4
    net, ln, labels, colors = getModel()
    
    for i in range(1, 5):
        vcap     = cv2.VideoCapture('snap/%s/%s-tesla%s.mp4' % (date_dir, date_dir, i))
        width  = int(vcap.get(3))  # float `width`
        height = int(vcap.get(4))  # float `height`
        #fps = vcap.get(cv2.CAP_PROP_FPS)
        fps = int(vcap.get(5))
        out = cv2.VideoWriter('snap/%s/%s-tesla%s-yolo.mp4' % (date_dir, date_dir, i), cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (width, height))
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
            out.write(frame)
            if key == ord('q'):
                sys.exit()
            if not ret:
                print("frame read failed")
                break

def main():
    cur_time = time.time()
    eventstart = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time))
    eventend = datetime.datetime.strptime(eventstart, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(days=1)
    eventdate = eventend.strftime('%Y-%m-%d %H:%M:%S')
    date_dir = eventdate[0:eventdate.index(' ')]
    print(date_dir)
    jpg2mp4(date_dir)
    #for f in glob.glob('snap/%s/*.jpg' % date_dir):
    #    os.remove(f)
    detect_video(date_dir)

if __name__ == '__main__':
    main()
