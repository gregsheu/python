import ffmpeg
import time 
import datetime
import os
import glob

def jpg2mp4(date_dir):
    for f in glob.glob('snap/%s/*.jpg' % date_dir):
        b = os.path.getsize(f)
        if b == 0:
            os.remove(f)
    (
        ffmpeg.input('snap/%s/tripsnap-1*.jpg' % date_dir, pattern_type='glob', framerate=1)
        .output('snap/%s/%s-tesla1.mp4' % (date_dir, date_dir), r=3)
        .overwrite_output()
        .run()
    )
    (
        ffmpeg.input('snap/%s/tripsnap-2*.jpg' % date_dir, pattern_type='glob', framerate=1)
        .output('snap/%s/%s-tesla2.mp4' % (date_dir, date_dir), r=3)
        .overwrite_output()
        .run()
    )
    (
        ffmpeg.input('snap/%s/tripsnap-3*.jpg' % date_dir, pattern_type='glob', framerate=1)
        .output('snap/%s/%s-tesla3.mp4' % (date_dir, date_dir), r=3)
        .overwrite_output()
        .run()
    )
    (
        ffmpeg.input('snap/%s/tripsnap-4*.jpg' % date_dir, pattern_type='glob', framerate=1)
        .output('snap/%s/%s-tesla4.mp4' % (date_dir, date_dir), r=3)
        .overwrite_output()
        .run()
    )

def main():
    cur_time = time.time()
    eventstart = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur_time))
    eventend = datetime.datetime.strptime(eventstart, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(days=1)
    eventdate = eventend.strftime('%Y-%m-%d %H:%M:%S')
    date_dir = eventdate[0:eventdate.index(' ')]
    jpg2mp4(date_dir)
    for f in glob.glob('snap/%s/*.jpg' % date_dir):
        os.remove(f)

if __name__ == '__main__':
    main()
