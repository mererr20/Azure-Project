import os
import datetime
import threading
import concurrent.futures
from audio import Audio
from frame import Frame
import math
from analyzer import *


'''
'''


def framesExtraction(path, videoName):
    video = Frame(path, videoName)
    video.thread()


'''
'''


def createMovieDirectories(videoName):
    try:
        if not os.path.exists('FinalResults'):
            os.makedirs('FinalResults')
        if not os.path.exists('Data'):
            os.makedirs('Data')
        if not os.path.exists('Data\\' + videoName):
            os.makedirs('Data\\' + videoName)
        if not os.path.exists('Data\\' + videoName + '\\frames'):
            os.makedirs('Data\\' + videoName + '\\frames')
        if not os.path.exists('Data\\' + videoName + '\\audio'):
            os.makedirs('Data\\' + videoName + '\\audio')
        if not os.path.exists('Data\\' + videoName + '\\temp'):
            os.makedirs('Data\\' + videoName + '\\temp')
    except OSError:
        print('Error: Creating directory of data')


'''
    Este método realiza la extracción del audio del video,
    además, lo fracciona en 4 por medio de la clase Audio.
'''


def audioExtraction(path, videoName):
    audio = Audio(path, videoName)
    audio.audioExtraction()
    audio.setAudio()
    audio.multipleSplit(math.ceil(audio.getDurationMinutes()/4))


'''
    Este método llama a los demás métodos encargados de
    realizar la extracción del audio y frames de un video.
'''


def startExtraction(path, video):
    audioExtraction(path, video)
    framesExtraction(path, video)
    return 'Extraction completed'


'''
'''


def extraction(videos, videoFolderPath):
    startTime = datetime.datetime.now()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futureVideo = {executor.submit(startExtraction, videoFolderPath, video.replace(
            '.mp4', '')): createMovieDirectories(video.replace('.mp4', '')) for video in videos}
        for future in concurrent.futures.as_completed(futureVideo):
            try:
                print(future.result())
            except Exception as exc:
                print('%r generated an exception: %s' % (future, exc))
    endTime = datetime.datetime.now()
    print('Time of the extraction method: {}'.format(endTime - startTime))



# {'Video':[]}
textAnalysis = []
emotionAnalysis = []

'''
'''


def analyzer(list, pos):
    for video in list:
        video = str(video).replace('.mp4', '')
        dataAudio = audioAnalyzer(video, pos)
        dataFrame = frameAnalyzer(video, pos)
        textAnalysis.append({video: dataAudio})
        emotionAnalysis.append({video: dataFrame})
    print('\n\n')
    print(list)
    print('\n\n')
    print(emotionAnalysis)
    print('\n\n')
    print(textAnalysis)


'''
'''


def distribution(listVideos):
    print(listVideos)
    size = len(listVideos)
    half = math.ceil(size / 2)
    listVideos1 = listVideos[0:half]
    listVideos2 = listVideos[half:size]
    print(listVideos1)
    print(listVideos2)
    print('\n\n')
    startTime = datetime.datetime.now()
    firstPart = threading.Thread(target=analyzer, args=(listVideos1, 0))
    secondPart = threading.Thread(target=analyzer, args=(listVideos2, 1))
    firstPart.start()
    secondPart.start()
    firstPart.join()
    secondPart.join()
    endTime = datetime.datetime.now()
    print('Time of the analyzer method: {}'.format(endTime - startTime))


def results():
    print('')


if __name__ == "__main__":
    folderPath = '.\\videos'
    nameVideos = os.listdir(folderPath)
    extraction(nameVideos, folderPath)
    distribution(nameVideos)
    # results()
