#import ffmpeg
#r = ffmpeg.input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(704, 480))
#
#(
#    ffmpeg
#    #For 704 size rate, 4096k, 8192k, g=1 r=3, by far the lowest latency
#    #.output(r, 'rtmp://%s/live/cam%s' % (server, cam), f='flv', vsync='vfr', r=15, vb='%s' % frate, vcodec='libx264', maxrate='%s' % frate, bufsize='%s' % brate, g=3, vf='scale=%s:trunc(ow/a/2)*2' % fsize, tune='zerolatency', preset='ultrafast')
#    .output(r, 'rtmp://192.168.1.160/live/cam1', f='flv', vsync='vfr', r=5, vb='512k', vcodec='libx264', maxrate='512k', bufsize='2048k', g=5, s='704x480', tune='zerolatency', preset='ultrafast')
#    .overwrite_output()
#    .run_async(pipe_stdin=True)
#)
#
import cv2

cap = cv2.VideoCapture('0 ! videoconvert ! appsink ! videoscale ! video/x-raw,width=640,height=480 ! x264enc ! mpegtsmux !', 0, 20, Size(800, 600), True)

while True:
    try:
        ret, frame = cap.read()
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) == ord('q'):
            break
    except Exception as e:
        print(e)
        break
cap.release()
cv2.destroyAllWindows()
