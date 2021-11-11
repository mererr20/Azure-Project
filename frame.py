import cv2
import math
import threading


class Frame():
    def __init__(self, path, filename):
        self.filename = filename
        self.filepath = path + '\\' + filename + '.mp4'
        self.video1 = cv2.VideoCapture(self.filepath)
        self.video2 = cv2.VideoCapture(self.filepath)

    def frameExtraction(self, video, start, end):
        while(start <= end):
            video.set(cv2.CAP_PROP_POS_MSEC, start)
            ret, frame = video.read()
            if(ret):
                newRoute = '.\\Data\\' + self.filename + '\\frames\\' + \
                    str(start) + '_' + self.filename + '.jpg'
                cv2.imwrite(newRoute, frame)
                cv2.waitKey(0)
                start += 2000
        video.release()
        cv2.destroyAllWindows()

    def getAmountFrames(self):
        return math.ceil(self.video1.get(cv2.CAP_PROP_FRAME_COUNT))

    def getAmountFPS(self):
        return math.ceil(self.video1.get(cv2.CAP_PROP_FPS))

    def getSeconds(self):
        return math.ceil(self.getAmountFrames() / self.getAmountFPS())

    def getMiliseconds(self):
        return math.ceil(self.getSeconds() * 1000)

    def thread(self, video, fromMin, toMin):
        videoThread = threading.Thread(
            target=self.frameExtraction, args=(video, fromMin, toMin))
        videoThread.start()
        videoThread.join()