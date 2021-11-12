import cv2
import concurrent.futures
from moviepy.editor import *

class Frame():
    def __init__(self, path, filename):
        self.filename = filename
        self.filepath = path + '\\' + filename + '.mp4'
        self.video1 = cv2.VideoCapture(self.filepath)
        self.video2 = cv2.VideoCapture(self.filepath)
        self.videos = [self.video1, self.video2]

    def frameExtraction(self, video, start, end):
        while(start <= end):
            video.set(cv2.CAP_PROP_POS_MSEC, start)
            ret, frame = video.read()
            newRoute = '.\\Data\\' + self.filename + '\\frames\\' + \
                str(start) + '_' + self.filename + '.jpg'
            if ret:
                cv2.imwrite(newRoute, frame)
                cv2.waitKey(0)
            start += 5000
        video.release()
        cv2.destroyAllWindows()

    def getAmountFrames(self):
        return int(self.video1.get(cv2.CAP_PROP_FRAME_COUNT))

    def getAmountFPS(self):
        return int(self.video1.get(cv2.CAP_PROP_FPS))

    def getSeconds(self):
        return int(VideoFileClip(self.filepath).duration)

    def getMiliseconds(self):
        return int(self.getSeconds() * 1000)

    def thread(self):
        half = int(self.getMiliseconds() / 2)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for x in range(0, 2):
                executor.submit(self.frameExtraction, self.videos[x], (x * half), (x + 1) * half)