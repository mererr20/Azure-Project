from pydub import AudioSegment
import math

class SplitWavAudioMubin():
    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename
        self.filepath = folder + '\\' + filename
        self.audio = AudioSegment.from_wav(self.filepath)
    
    def getDuration(self):
        return self.audio.duration_seconds
    
    def singleSplit(self, from_min, to_min, split_filename):
        t1 = from_min * 60 * 1000
        t2 = to_min * 60 * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export('Data\\' + self.filename.replace('.wav','') + '\\audio\\' + split_filename + '.wav', format="wav")
        
    def multipleSplit(self, min_per_split):
        total_mins = math.ceil(self.getDuration() / 60)
        for i in range(0, total_mins, min_per_split):
            split_fn = str(i) + '_audio'
            self.singleSplit(i, i + min_per_split, split_fn)
            print(str(i) + ' Done')
            if i == total_mins - min_per_split:
                print('All splited successfully')