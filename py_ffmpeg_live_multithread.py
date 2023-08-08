import threading
import ffmpeg
import os
import json
import multiprocessing as mp

def run_ffmpeg(ip, channel, server, cam):
    #Change NVR encoding to 1280x720 15FPS 1024k; 704x480 15FPS 256k, r=15, g=3 to have lowest latency
    #With FRATE=8192k BRATE=16384k FSIZE=1280 to have STREAM=0 r=5, g=1 best resolution and low latency
    #With FRATE=4096k BRATE=8192k FSIZE=640 to have STREAM=1 r=5, g=1 best resolution and low latency
    frate = os.getenv('FRATE')
    brate = os.getenv('BRATE')
    #704x480, 640x480, 354x240
    fsize = os.getenv('FSIZE')
    stream = os.getenv('STREAM')
    #onview-2
    #r = ffmpeg.input('rtsp://admin:admin12345@107.127.238.14:554/cam/realmonitor?channel=%s&subtype=%s' % (cam, stream), rtsp_transport='tcp')
    #onview-1
    #r = ffmpeg.input('rtsp://admin:admin12345@107.127.237.29:554/cam/realmonitor?channel=%s&subtype=%s' % (cam, stream), rtsp_transport='tcp')
    #onview-3
    #r = ffmpeg.input('rtsp://admin:admin12345@107.127.237.43:554/cam/realmonitor?channel=%s&subtype=%s' % (cam, stream), rtsp_transport='tcp')
    r = ffmpeg.input('rtsp://admin:admin12345@%s:554/cam/realmonitor?channel=%s&subtype=%s' % (ip, channel, stream), rtsp_transport='tcp')
    (
        ffmpeg
        #For 704 size rate, 4096k, 8192k, g=1 r=3, by far the lowest latency
        #.output(r, 'rtmp://%s/live/cam%s' % (server, cam), f='flv', vsync='vfr', r=15, vb='%s' % frate, vcodec='libx264', maxrate='%s' % frate, bufsize='%s' % brate, g=3, vf='scale=%s:trunc(ow/a/2)*2' % fsize, tune='zerolatency', preset='ultrafast')
        .output(r, 'rtmp://%s/live/%s-cam%s' % (server, ip, cam), f='flv', vsync='vfr', r=5, vb='%s' % frate, vcodec='libx264', maxrate='%s' % frate, bufsize='%s' % brate, g=10, s='%s' % fsize, preset='slow')
        #.output(r, 'rtmp://%s/live/cam%s' % (server, cam), f='flv', vsync='vfr', vcodec='libx264', s='704x480', tune='zerolatency', preset='ultrafast')
        .overwrite_output()
        .run()
    )

def main():
    server = os.getenv('SERVER')
    context = {}
    gps_file = open('onview.json')
    gps_json = json.loads(gps_file.read())
    for i in gps_json:
        context.update({i['ip']: {'lat': i['lat'], 'lon': i['lon'], 'address': i['address']}})
    address = list({'id': k.replace('.', ''), 'ip': str(k), 'lat': v['lat'], 'lon': v['lon'], 'address': v['address']} for k, v in context.items())
    n_threads = len(address) * 4 + 1
    # Splitting the items into chunks equal to number of threads
    thread_list = []
    for i in address:
        print(i['ip'])
    #mp.set_start_method(method='spawn')
    #queues = [mp.Queue(maxsize=4) for i in cameras_ip]
    #processes = []
    #for queue, ip in zip(queues, cameras_ip):
    #    print(queue, ip)
    #    processes.append(mp.Process(target=run_ffmpeg, args=(ip, 1, server, 1)))
    #    processes.append(mp.Process(target=run_ffmpeg, args=(ip, 2, server, 2)))
    #    processes.append(mp.Process(target=run_ffmpeg, args=(ip, 3, server, 3)))
    #    processes.append(mp.Process(target=run_ffmpeg, args=(ip, 4, server, 4)))
    #for process in processes:
    #    process.daemon = True
    #    process.start()
    #for process in processes:
    #    process.join()
        ip = i['ip']
        t = i['id'] + '1'
        print(t)
        t = threading.Thread(target=run_ffmpeg, args=(ip, 1, server, 1,))
        t.start()
        t = i['id'] + '2'
        t = threading.Thread(target=run_ffmpeg, args=(ip, 2, server, 2,))
        t.start()
        t = i['id'] + '3'
        t = threading.Thread(target=run_ffmpeg, args=(ip, 3, server, 3,))
        t.start()
        t = i['id'] + '4'
        t = threading.Thread(target=run_ffmpeg, args=(ip, 4, server, 4,))
        t.start()

if __name__ == '__main__':
    main()
