import cv2
import numpy as np

class VideoCaptureYUV:
    def __init__(self, filename, size):
        self.height, self.width = size
        self.frame_len = int(self.width*self.height*1.5)
        self.f = open(filename, 'rb')
        self.shape = (int(self.height*1.5), self.width)

    def read_raw(self):
        try:
            raw = self.f.read(self.frame_len)
            print('This is frame_len %s' % self.frame_len)
            print('This is raw_len %s' % len(raw))
            yuv = np.frombuffer(raw, dtype=np.uint8)
            yuv = yuv.reshape(self.shape)
        except Exception as e:
            print(str('This is %s' % e))
            return False, None
        return True, yuv

    def read(self):
        ret, yuv = self.read_raw()
        if not ret:
            return ret, yuv
        #bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_NV21)
        bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)
        return ret, bgr


if __name__ == "__main__":
    filename = "dahuasdk/Demo/RealPlayDemo/data.yuv"
    #filename = "./chevvy.yuv"
    #filename = "./akiyo_cif.yuv"
    #size = (240, 352)
    #filename = "./testyuv.yuv"
    size = (576, 704)
    #size = (480, 704)
    #size = (1080, 1920)
    cap = VideoCaptureYUV(filename, size)

    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("frame", frame)
            cv2.waitKey(1)
        else:
            break
