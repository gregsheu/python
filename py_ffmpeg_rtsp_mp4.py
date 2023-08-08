import ffmpeg
for i in range(1, 3):
    #r1 = ffmpeg.input('rtsp://admin:admin12345@166.193.32.146:554/cam/realmonitor?channel=%s&subtype=0' % i, rtsp_transport = 'tcp')
    #r1 = ffmpeg.input('rtsp://admin:admin12345@166.193.32.146:554/cam/playback?channel=%i&starttime=2022_06_20_12_00_00&endtime=2022_06_20_12_01_00' % i, rtsp_transport='tcp', r=5)
    #r1 = ffmpeg.input('rtsp://ADMIN:Qqq12345@63.42.254.148:554/rtspstream?channel=2&stream=0')
    r1 = ffmpeg.input('rtsp://ADMIN:Qqq12345@192.168.0.108:554/rtspstream?channel=2&stream=0')
    (
        ffmpeg
        #.input('rtsp://admin:admin12345@166.144.52.64:554/cam/realmonitor?channel=4&subtype=0', rtsp_transport='tcp')
        #.output(r1, '%s.mp4' % i, f='mp4', vsync='vfr', r=5, vb='256k', codec='copy', maxrate='256k', bufsize='512k', g=10, s='704x480', preset='ultrafast')
        .output(r1, '%s.mp4' % i, ss=0, t=20)
        #.output(r1, '%s.mp4' % i, f='mp4', r=5, vcodec='libx264', acodec='copy', g=10, s='1920x1080', preset='ultrafast')
        #.output(r1, '%s.mp4' % i, f='mp4', r=5, vcodec='libx264', acodec='copy', g=10, s='1920x1080', preset='ultrafast')
        .overwrite_output()
        .run()
    )

#r1 = ffmpeg.input('rtsp-1.jpg')
#r2 = ffmpeg.input('rtsp-2.jpg')
#r3 = ffmpeg.input('rtsp-3.jpg')
#r4 = ffmpeg.input('rtsp-4.jpg')
#(
#    ffmpeg
#    .filter('xstack', 4, '0_0|0_h0|w0_0|w0_h0')
#    .output((r1, r2, r3, r4), 'rtsp-s.jpg', vframes=1)
#    .overwrite_output()
#    .run()
#)
