## WS client example
import asyncio
import multiprocessing
import threading
import websockets
import socketserver
import multiprocessing
import cv2
import sys
import ffmpeg
from datetime import datetime as dt

PROCESSES = []
def camera(jpegs):
    #vc = cv2.VideoCapture(0)
    vc = cv2.VideoCapture('rtsp://admin:admin12345@192.168.1.115:554/cam/realmonitor?channel=1&subtype=0')
    #vc = cv2.VideoCapture('rtsp://admin:admin12345@107.127.237.43:554/cam/realmonitor?channel=2&subtype=0')
    if vc.isOpened():
        r, f = vc.read()
    else:
        r = False
    while r:
        cv2.waitKey(20)
        r, f = vc.read()
        #f = cv2.resize(f, (704, 576))
        f = cv2.resize(f, (1920, 1080))
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 85]
        jpegs[0] = (cv2.imencode('.jpg', f, encode_param)[1])
        #return jpeg[0]

def socket(jpegs):
    async def handler(websocket, path):
        try:
            while True:
                #jpeg = camera()
                await asyncio.sleep(0.025)
                await websocket.send(jpegs[0].tobytes())
        except websockets.exceptions.ConnectionClosed:
            print("Socket closed")
    start_server = websockets.serve(handler, '0.0.0.0', 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
    
def client():
    async def handler():
        uri = 'ws://0.0.0.0:8765'
        async with websockets.connect(uri) as websocket:
            #name = input("What's your name? ")
            try:
                while True:
                    jpg = camera()
                    await websocket.send(jpg.tobytes())
            except websockets.exceptions.ConnectionClosed:
                print("Failed cams")

def main():
    manager = multiprocessing.Manager()
    jpeg = manager.list()
    jpeg.append(None)
    t1 = multiprocessing.Process(target=camera, args=(jpeg,))
    #t2 = multiprocessing.Process(target=socket, args=(jpeg,))
    PROCESSES.append(t1)
    #PROCESSES.append(t2)
    for p in PROCESSES:
        p.start()
    # Wait forever
    while True:
        pass
    #t1.join()
    #t2.join()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        for p in PROCESSES:
            p.terminate()
