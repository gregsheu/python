import threading
import ffmpeg

def run_ffmpeg(ip, channel, cam):
    r = ffmpeg.input('rtsp://admin:admin12345@192.168.1.%s:554/cam/realmonitor?channel=%s&subtype=0' % (ip, channel), rtsp_transport='tcp')
    (
        ffmpeg
        .output(r, 'rtmp://localhost/live/cam%s' % cam, flvflags='no_duration_filesize', f='flv', vsync='vfr', r=25, vb='4096k', vcodec='libx264', maxrate='4096k', bufsize='8192k', g=50, pix_fmt='yuvj420p', vf='scale=720:trunc(ow/a/2)*2', tune='zerolatency', preset='ultrafast', crf=23)
        .overwrite_output()
        .run()
    )

def main():
    t1 = threading.Thread(target=run_ffmpeg, args=(77, 1, 1,))
    t2 = threading.Thread(target=run_ffmpeg, args=(78, 1, 2,))
    t3 = threading.Thread(target=run_ffmpeg, args=(107, 1, 3,))
    t4 = threading.Thread(target=run_ffmpeg, args=(238, 1, 4,))
    #t5 = threading.Thread(target=run_ffmpeg, args=(109, 3,5,))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    #t5.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    #t5.join()

if __name__ == '__main__':
    main()
