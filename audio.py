from pydub import AudioSegment
import moviepy.editor as me
import math


class Audio():
    def __init__(self, path, filename):
        self.path = path
        self.filename = filename
        self.filepath = 'Data\\' + filename + '\\temp\\' + (filename + '.wav')
        self.audio = ''

    def setAudio(self):
        self.audio = AudioSegment.from_wav(self.filepath)

    def getDurationSeconds(self):
        return self.audio.duration_seconds

    def getDurationMinutes(self):
        return int(self.getDurationSeconds() / 60)

    def singleSplit(self, fromMin, toMin, splitFilename):
        t1 = fromMin * 60 * 1000
        t2 = toMin * 60 * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export('Data\\' + self.filename +
                           '\\audio\\' + splitFilename + '.wav', format="wav")

    def multipleSplit(self, minSplit):
        totalMins = self.getDurationMinutes()
        for i in range(0, totalMins, minSplit):
            split = str(i) + '_audio'
            self.singleSplit(i, i + minSplit, split)
            print(str(i) + ' Done')
        print('All splited successfully')

    def audioExtraction(self):
        print("Converting...")
        video = me.VideoFileClip((self.path + '\\' + self.filename + '.mp4'))
        video.audio.write_audiofile(
            ('Data\\' + self.filename + '\\temp\\' + self.filename + '.wav'))
