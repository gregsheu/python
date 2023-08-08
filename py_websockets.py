## WS client example
import asyncio
import multiprocessing
import threading
import websockets
import socketserver
import multiprocessing
import cv2
import sys
from datetime import datetime as dt

PROCESSES = []
def camera(jpegs, ip, channel):
    #vc = cv2.VideoCapture(0)
    #vc = cv2.VideoCapture('rtsp://admin:admin12345@192.168.1.108:554/cam/realmonitor?channel=2&subtype=0')
    vc = cv2.VideoCapture('rtsp://admin:admin12345@%s:554/cam/realmonitor?channel=%s&subtype=0' % (ip, channel))
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

def socket(jpegs, socket):
    async def handler(websocket, path):
        try:
            while True:
                #jpeg = camera()
                await asyncio.sleep(0.025)
                await websocket.send(jpegs[0].tobytes())
        except websockets.exceptions.ConnectionClosed:
            print("Socket closed")
    start_server = websockets.serve(handler, '0.0.0.0', socket)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
    
def main():
    manager = multiprocessing.Manager()
    jpeg1 = manager.list()
    jpeg2 = manager.list()
    jpeg3 = manager.list()
    jpeg4 = manager.list()
    jpeg1.append(None)
    jpeg2.append(None)
    jpeg3.append(None)
    jpeg4.append(None)
    t1 = multiprocessing.Process(target=camera, args=(jpeg1, '107.127.238.14', 1,))
    t2 = multiprocessing.Process(target=camera, args=(jpeg2, '107.127.238.14', 2,))
    t3 = multiprocessing.Process(target=camera, args=(jpeg3, '107.127.238.14', 3,))
    t4 = multiprocessing.Process(target=camera, args=(jpeg4, '107.127.238.14', 4,))
    t5 = multiprocessing.Process(target=socket, args=(jpeg1, 8765,))
    t6 = multiprocessing.Process(target=socket, args=(jpeg2, 8766,))
    t7 = multiprocessing.Process(target=socket, args=(jpeg3, 8767,))
    t8 = multiprocessing.Process(target=socket, args=(jpeg4, 8768,))
    PROCESSES.append(t1)
    PROCESSES.append(t2)
    PROCESSES.append(t3)
    PROCESSES.append(t4)
    PROCESSES.append(t5)
    PROCESSES.append(t6)
    PROCESSES.append(t7)
    PROCESSES.append(t8)
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
