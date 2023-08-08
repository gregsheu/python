# WS server example
import asyncio
import websockets
import socketserver
from datetime import datetime as dt

def log(message):
    print("[LOG] " + str(dt.now()) + " - " + message)

async def hello(websocket, path):
    try:
        while True:
            await asyncio.sleep(0.025) # 25 fps
            #await websocket.recv()
            await websocket.recv()
            #with open('tt.jpg', 'wb') as f:
            #    f.write((jpegs))
            #await websocket.send(jpegs)
            
    except websockets.exceptions.ConnectionClosed:
        log("Socket closed")
    #print(f"< {name}")

    #greeting = f"Hello {name}!"

    #await websocket.send(greeting)
    #print(f"> {greeting}")

start_server = websockets.serve(hello, "0.0.0.0", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
