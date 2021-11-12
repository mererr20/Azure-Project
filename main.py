import os
import datetime
import threading
import concurrent.futures
from audio import Audio
from frame import Frame
import math
from analyzer import *
from test import *

# {'Video':[]}
textAnalysis = {}
sceneAnalysis = {}
emotionAnalysis = {}

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
'''


def framesExtraction(path, videoName):
    video = Frame(path, videoName)
    video.thread()


'''
    Este método realiza la extracción del audio del video,
    además, lo fracciona en 4 por medio de la clase Audio.
'''


def audioExtraction(path, videoName):
    audio = Audio(path, videoName)
    audio.audioExtraction()
    audio.setAudio()
    audio.multipleSplit(int(audio.getDurationMinutes()/2))


'''
    Este método llama a los demás métodos encargados de
    realizar la extracción del audio y frames de un video.
'''


def startExtraction(path, video):
    audioExtraction(path, video)
    framesExtraction(path, video)
    print('Extraction completed')


'''
'''


def extraction(videos, videoFolderPath):
    startTime = datetime.datetime.now()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futureVideo = {executor.submit(startExtraction, videoFolderPath, video.replace(
            '.mp4', '')): video for video in videos}
        for future in concurrent.futures.as_completed(futureVideo):
            try:
                print(future.result())
            except Exception as exc:
                print('%r generated an exception: %s' % (future, exc))
    endTime = datetime.datetime.now()
    print('Time of the extraction method: {}'.format(endTime - startTime))


'''
'''


def analyzer(list, pos):
    for video in list:
        video = str(video).replace('.mp4', '')
        dataAudio = audioAnalyzer(video, pos)
        dataFrame = frameDistribution(video, pos)

        textAnalysis[video] = [dataAudio]
        emotionAnalysis[video] = dataFrame[0]
        sceneAnalysis[video] = dataFrame[1]

    print('\n\n')
    print(list)
    print('\n\n')
    print(emotionAnalysis)
    print('\n\n')
    print(sceneAnalysis)
    print('\n\n')
    print(textAnalysis)


'''
'''


def distribution(listVideos):
    print(listVideos)
    size = len(listVideos)
    half = math.ceil(size / 2)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        a = 2
        if size == 1:
            a = 1
        for x in range(0, a):
            list = listVideos[(x * half): ((x + 1) * half)]
            executor.submit(analyzer, list, x)


def results(listVideos):

    for video in listVideos:

        video = str(video).replace('.mp4', '')

        for audio in textAnalysis[video]:
            print(audio.confidence_scores.positive,
                  audio.confidence_scores.neutral, audio.confidence_scores.negative)

        for face in emotionAnalysis[video]:
            if face != '':
                print(f"->     Azure id: {face.face_id}")
                print(f"->     Detected age: {face.face_attributes.age}")
                print(f"->     Detected gender: {face.face_attributes.gender}")
                print(
                    f"->     Detected emotion: {face.face_attributes.emotion}")
                print(f"->     Anger: {face.face_attributes.emotion.anger}")

        for scene in sceneAnalysis[video]:
            print(scene.adult.is_adult_content)


if __name__ == "__main__":
    print('Welcome to the analyzer!')
    folderPath = '.\\videos'  # Address of the folder to analyze
    nameVideos = os.listdir(folderPath)
    for video in nameVideos:
        createMovieDirectories(video.replace('.mp4', ''))
    extraction(nameVideos, folderPath)
    distribution(nameVideos)
    results(nameVideos)
