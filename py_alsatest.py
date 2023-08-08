import alsaaudio
import wave

if __name__ == '__main__':

    out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, channels=2, rate=11025, format=alsaaudio.PCM_FORMAT_S16_LE)
    # Read data from stdin
    f = open('/tmp/alarm.wav', 'rb')
    data = f.read(32)
    while data:
        out.write(data)
        data = f.read(32)
