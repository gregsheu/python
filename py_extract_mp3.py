import ffmpeg
v = ffmpeg.input('/sambashare/20220209_131354.mp4')
a = v.audio
(
    ffmpeg
    #.output(a, '/sambashare/recorded.mp3', ss=0, t=207)
    .output(a, '/sambashare/recorded.mp3', ss=0, t=207)
    .overwrite_output()
    .run()
)

