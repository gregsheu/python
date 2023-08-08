import ffmpeg

def stitch_video(in1, in2, in3):
    v1 = ffmpeg.input(in1)
    v2 = ffmpeg.input(in2)
    v3 = ffmpeg.input(in3)
    (
        ffmpeg
        .concat(
            v1,
            v2,
            v3,
        )
        .filter('scale', '1920', '1080')
        .filter('setsar', sar=1/1)
        .output('stitch_all3.mp4', r=25)
        .overwrite_output()
        .run()
    )

def main():
    in1 = 'stitch_all.mp4'
    in2 = 'stitch_all_1.mp4'
    in3 = 'stitch_all_2.mp4'
    stitch_video(in1, in2, in3)

if __name__ == '__main__':
    main()
