# WS client example
import asyncio
import pickle
import websockets
import socketserver
import multiprocessing
import cv2
import sys
from datetime import datetime as dt
def camera():
    #vc = cv2.VideoCapture(0)
    #vc = cv2.VideoCapture('rtsp://admin:admin12345@192.168.1.115:554/cam/realmonitor?channel=1&subtype=1')
    vc = cv2.VideoCapture('rtsp://admin:admin12345@192.168.1.115:554/cam/realmonitor?channel=1&subtype=0')
    if vc.isOpened():
        r, f = vc.read()
    else:
        r = False
    while r:
        cv2.waitKey(20)
        r, f = vc.read()
        #f = cv2.resize(f, (704, 576))
        #f = cv2.resize(f, (704, 480))
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]
        jpeg = []
        jpeg.append(cv2.imencode('.jpg', f, encode_param)[1])
        return jpeg[0]


async def hello():
    uri = 'ws://kingsolarmaniot.dvrlists.com:8765'
    async with websockets.connect(uri) as websocket:
        #name = input("What's your name? ")
        try:
            while True:
                jpg = camera()
                await websocket.send(jpg.tobytes())
        except websockets.exceptions.ConnectionClosed:
            print("Failed cams")

asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()
