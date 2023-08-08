import ffmpeg

#for i in range(2, 3):
#    if i < 10:
#        (
#            ffmpeg.input('/tmp/2021-06-0%s/tripsnap-1*.jpg' % i, pattern_type='glob', framerate=1)
#            #.crop(0, 0, 1280, 720)
#            .filter('scale',1280, 720)
#            .filter('setsar', sar=1/1)
#            .drawtext('Created by G.S. @King Solarman Inc.', 10, 700, fontcolor='red', fontsize=24, fontfile='/usr/share/fonts/truetype/freefont/FreeSansBold.ttf')
#            .output('ks-gif.mp4', r=29.97)
#            .overwrite_output()
#            .run()
#        )
#        (  
#            ffmpeg.input('ks-gif.mp4')
#            .setpts('0.054*PTS')
#            .output('%s-1.mp4' % i)
#            .overwrite_output()
#            .run()
#        )
#        
#        (
#            ffmpeg.input('/tmp/2021-06-0%s/tripsnap-2*.jpg' % i, pattern_type='glob', framerate=1)
#            #.crop(0, 0, 1280, 720)
#            .filter('scale',1280, 720)
#            .filter('setsar', sar=1/1)
#            .drawtext('Created by G.S. @King Solarman Inc.', 10, 700, fontcolor='red', fontsize=24, fontfile='/usr/share/fonts/truetype/freefont/FreeSansBold.ttf')
#            .output('ks-gif.mp4', r=29.97)
#            .overwrite_output()
#            .run()
#        )
#        (  
#            ffmpeg.input('ks-gif.mp4')
#            .setpts('0.054*PTS')
#            .output('%s-2.mp4' % i)
#            .overwrite_output()
#            .run()
#        )
#        
#        (
#            ffmpeg.input('/tmp/2021-06-0%s/tripsnap-3*.jpg' % i, pattern_type='glob', framerate=1)
#            #.crop(0, 0, 1280, 720)
#            .filter('scale',1280, 720)
#            .filter('setsar', sar=1/1)
#            .drawtext('Created by G.S. @King Solarman Inc.', 10, 700, fontcolor='red', fontsize=24, fontfile='/usr/share/fonts/truetype/freefont/FreeSansBold.ttf')
#            .output('ks-gif.mp4', r=29.97)
#            .overwrite_output()
#            .run()
#        )
#        (  
#            ffmpeg.input('ks-gif.mp4')
#            .setpts('0.054*PTS')
#            .output('%s-3.mp4' % i)
#            .overwrite_output()
#            .run()
#        )
#        
#        (
#            ffmpeg.input('/tmp/2021-06-0%s/tripsnap-4*.jpg' % i, pattern_type='glob', framerate=1)
#            #.crop(0, 0, 1280, 720)
#            .filter('scale',1280, 720)
#            .filter('setsar', sar=1/1)
#            .drawtext('Created by G.S. @King Solarman Inc.', 10, 700, fontcolor='red', fontsize=24, fontfile='/usr/share/fonts/truetype/freefont/FreeSansBold.ttf')
#            .output('ks-gif.mp4', r=29.97)
#            .overwrite_output()
#            .run()
#        )
#        (  
#            ffmpeg.input('ks-gif.mp4')
#            .setpts('0.054*PTS')
#            .output('%s-4.mp4' % i)
#            .overwrite_output()
#            .run()
#        )
#    else:
#        (
#            ffmpeg.input('/tmp/2021-06-%s/tripsnap-1*.jpg' % i, pattern_type='glob', framerate=1)
#            #.crop(0, 0, 1280, 720)
#            .filter('scale',1280, 720)
#            .filter('setsar', sar=1/1)
#            .drawtext('Created by G.S. @King Solarman Inc.', 10, 700, fontcolor='red', fontsize=24, fontfile='/usr/share/fonts/truetype/freefont/FreeSansBold.ttf')
#            .output('ks-gif.mp4', r=29.97)
#            .overwrite_output()
#            .run()
#        )
#        (  
#            ffmpeg.input('ks-gif.mp4')
#            .setpts('0.054*PTS')
#            .output('%s-1.mp4' % i)
#            .overwrite_output()
#            .run()
#        )
#        
#        (
#            ffmpeg.input('/tmp/2021-06-%s/tripsnap-2*.jpg' % i, pattern_type='glob', framerate=1)
#            #.crop(0, 0, 1280, 720)
#            .filter('scale',1280, 720)
#            .filter('setsar', sar=1/1)
#            .drawtext('Created by G.S. @King Solarman Inc.', 10, 700, fontcolor='red', fontsize=24, fontfile='/usr/share/fonts/truetype/freefont/FreeSansBold.ttf')
#            .output('ks-gif.mp4', r=29.97)
#            .overwrite_output()
#            .run()
#        )
#        (  
#            ffmpeg.input('ks-gif.mp4')
#            .setpts('0.054*PTS')
#            .output('%s-2.mp4' % i)
#            .overwrite_output()
#            .run()
#        )
#        
#        (
#            ffmpeg.input('/tmp/2021-06-%s/tripsnap-3*.jpg' % i, pattern_type='glob', framerate=1)
#            #.crop(0, 0, 1280, 720)
#            .filter('scale',1280, 720)
#            .filter('setsar', sar=1/1)
#            .drawtext('Created by G.S. @King Solarman Inc.', 10, 700, fontcolor='red', fontsize=24, fontfile='/usr/share/fonts/truetype/freefont/FreeSansBold.ttf')
#            .output('ks-gif.mp4', r=29.97)
#            .overwrite_output()
#            .run()
#        )
#        (  
#            ffmpeg.input('ks-gif.mp4')
#            .setpts('0.054*PTS')
#            .output('%s-3.mp4' % i)
#            .overwrite_output()
#            .run()
#        )
#        
#        (
#            ffmpeg.input('/tmp/2021-06-%s/tripsnap-4*.jpg' % i, pattern_type='glob', framerate=1)
#            #.crop(0, 0, 1280, 720)
#            .filter('scale',1280, 720)
#            .filter('setsar', sar=1/1)
#            .drawtext('Created by G.S. @King Solarman Inc.', 10, 700, fontcolor='red', fontsize=24, fontfile='/usr/share/fonts/truetype/freefont/FreeSansBold.ttf')
#            .output('ks-gif.mp4', r=29.97)
#            .overwrite_output()
#            .run()
#        )
#        (  
#            ffmpeg.input('ks-gif.mp4')
#            .setpts('0.054*PTS')
#            .output('%s-4.mp4' % i)
#            .overwrite_output()
#            .run()
#        )
#
i0 = ffmpeg.input('2-1.mp4')
i1 = ffmpeg.input('0603-1.mp4')
i2 = ffmpeg.input('0604-1.mp4')
i3 = ffmpeg.input('0605-1.mp4')
i4 = ffmpeg.input('0606-1.mp4')
i5 = ffmpeg.input('0607-1.mp4')
i6 = ffmpeg.input('0608-1.mp4')
i7 = ffmpeg.input('9-1.mp4')
i8 = ffmpeg.input('10-1.mp4')
i9 = ffmpeg.input('11-1.mp4')
i10 = ffmpeg.input('12-1.mp4')
i11 = ffmpeg.input('13-1.mp4')
i12 = ffmpeg.input('14-1.mp4')
(  
    ffmpeg
    .concat 
    (
        i0,
        i1, 
        i2,
        i3,
        i4,
        i5,
        i6,
        i7,
        i8,
        i9,
        i10,
        i11,
        i12,
    )
    .setpts('0.5*PTS')
    .output('i-11.mp4')
    .overwrite_output()
    .run()
)

i0 = ffmpeg.input('2-2.mp4')
i1 = ffmpeg.input('0603-2.mp4')
i2 = ffmpeg.input('0604-2.mp4')
i3 = ffmpeg.input('0605-2.mp4')
i4 = ffmpeg.input('0606-2.mp4')
i5 = ffmpeg.input('0607-2.mp4')
i6 = ffmpeg.input('0608-2.mp4')
i7 = ffmpeg.input('9-2.mp4')
i8 = ffmpeg.input('10-2.mp4')
i9 = ffmpeg.input('11-2.mp4')
i10 = ffmpeg.input('12-2.mp4')
i11 = ffmpeg.input('13-2.mp4')
i12 = ffmpeg.input('14-2.mp4')
(  
    ffmpeg
    .concat 
    (
        i0,
        i1, 
        i2,
        i3,
        i4,
        i5,
        i6,
        i7,
        i8,
        i9,
        i10,
        i11,
        i12,
    )
    .setpts('0.5*PTS')
    .output('i-12.mp4')
    .overwrite_output()
    .run()
)
i0 = ffmpeg.input('2-3.mp4')
i1 = ffmpeg.input('0603-3.mp4')
i2 = ffmpeg.input('0604-3.mp4')
i3 = ffmpeg.input('0605-3.mp4')
i4 = ffmpeg.input('0606-3.mp4')
i5 = ffmpeg.input('0607-3.mp4')
i6 = ffmpeg.input('0608-3.mp4')
i7 = ffmpeg.input('9-3.mp4')
i8 = ffmpeg.input('10-3.mp4')
i9 = ffmpeg.input('11-3.mp4')
i10 = ffmpeg.input('12-3.mp4')
i11 = ffmpeg.input('13-3.mp4')
i12 = ffmpeg.input('14-3.mp4')
(  
    ffmpeg
    .concat 
    (
        i0, 
        i1, 
        i2,
        i3,
        i4,
        i5,
        i6,
        i7,
        i8,
        i9,
        i10,
        i11,
        i12,
    )
    .setpts('0.5*PTS')
    .output('i-13.mp4')
    .overwrite_output()
    .run()
)
i0 = ffmpeg.input('2-4.mp4')
i1 = ffmpeg.input('0603-4.mp4')
i2 = ffmpeg.input('0604-4.mp4')
i3 = ffmpeg.input('0605-4.mp4')
i4 = ffmpeg.input('0606-4.mp4')
i5 = ffmpeg.input('0607-4.mp4')
i6 = ffmpeg.input('0608-4.mp4')
i7 = ffmpeg.input('9-4.mp4')
i8 = ffmpeg.input('10-4.mp4')
i9 = ffmpeg.input('11-4.mp4')
i10 = ffmpeg.input('12-4.mp4')
i11 = ffmpeg.input('13-4.mp4')
i12 = ffmpeg.input('14-4.mp4')
(  
    ffmpeg
    .concat 
    (
        i0, 
        i1, 
        i2,
        i3,
        i4,
        i5,
        i6,
        i7,
        i8,
        i9,
        i10,
        i11,
        i12,
    )
    .setpts('0.5*PTS')
    .output('i-14.mp4')
    .overwrite_output()
    .run()
)

