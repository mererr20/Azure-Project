import os
import datetime
import concurrent.futures
from audio import Audio
from frame import Frame
import math
from analyzer import *
from matplotlib import pyplot

textAnalysis = {}
sceneAnalysis = {}
emotionAnalysis = {}
timeProcesses = {}

'''
    Método para crear el directorio necesario para el control de
    los archivos.
'''
def createMovieDirectories(videoName):
    try:
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
        if not os.path.exists('Data\\' + videoName + '\\results'):
            os.makedirs('Data\\' + videoName + '\\results')
    except OSError:
        print('Error: Creating directory of data')


'''
    Este método realiza la extracción de los fotogramas del video,
    además, lo fracciona en 2 por medio de la clase Frame.

'''
def framesExtraction(path, videoName):
    video = Frame(path, videoName)
    video.thread()


'''
    Este método realiza la extracción del audio del video,
    además, lo fracciona en 2 por medio de la clase Audio.
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
    Método intermedio para obtener los datos de los diferentes
    vídeos.
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
    format = endTime - startTime
    timeProcesses['Extraction'] = format


'''
    Método para realizar el análisis de los datos,
    tanto de fotogramas como de audios.
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
    Método intermedio para comenzar con el análisis de
    los datos de los videos. En este método se asigna
    qué api consultar.
'''
def distribution(listVideos):
    print(listVideos)
    size = len(listVideos)
    half = math.ceil(size / 2)
    startTime = datetime.datetime.now()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        a = 2
        if size == 1:
            a = 1
        for x in range(0, a):
            list = listVideos[(x * half): ((x + 1) * half)]
            executor.submit(analyzer, list, x)
    endTime = datetime.datetime.now()
    format = endTime - startTime
    timeProcesses['Analysis'] = format


'''
    Método para obtener todos los resultados obtenidos luego
    del análisis del mismo.
'''
def results(listVideos):
    for v in listVideos:
        video = str(v).replace('.mp4', '')
        route = 'Data\\' + video + '\\results\\'
        age = []
        adultContent = 0
        gender = [0, 0]
        audioScore = []
        emotions = [0, 0, 0, 0, 0, 0, 0, 0]
        sceneCount = 0
        faceCount = 0

        for audio in textAnalysis[video]:
            if(audio != ''):
                audioScore.append(audio.confidence_scores.positive*100)
                audioScore.append(audio.confidence_scores.neutral*100)
                audioScore.append(audio.confidence_scores.negative*100)

        for face in emotionAnalysis[video]:
            if face != '':
                age.append(face.face_attributes.age)
                if face.face_attributes.gender == 'female':
                    gender[0] = gender[0] + 1
                else:
                    gender[1] = gender[1] + 1
                emotions[0] = emotions[0] + face.face_attributes.emotion.anger
                emotions[1] = emotions[1] + \
                    face.face_attributes.emotion.contempt
                emotions[2] = emotions[2] + \
                    face.face_attributes.emotion.disgust
                emotions[3] = emotions[3] + face.face_attributes.emotion.fear
                emotions[4] = emotions[4] + \
                    face.face_attributes.emotion.happiness
                emotions[5] = emotions[5] + \
                    face.face_attributes.emotion.neutral
                emotions[6] = emotions[6] + \
                    face.face_attributes.emotion.sadness
                emotions[7] = emotions[7] + \
                    face.face_attributes.emotion.surprise
                faceCount += 1

        with open(route + 'scenes.txt', 'a', 1) as file:
            file.write('Video: ' + video + '\n')
            age.sort()
            file.write('Age range: ' + str(age[0]) + ' to ' + str(age[len(age)-1]) + '\n')
            file.write('Scenarios found: ' + '\n')

        for scene in sceneAnalysis[video]:
            if scene != '':
                if(scene.adult.is_adult_content):
                    adultContent += 1
                if(scene.description.captions):
                    for caption in scene.description.captions:
                        with open(route + 'scenes.txt', 'a', 1) as file:
                            file.write('- ' + caption.text + '\n')
                sceneCount += 1

        with open(route + 'scenes.txt', 'a', 1) as file:
            if sceneCount != 0:
                file.write('Adult content: ' +
                        str(((adultContent/sceneCount)*100)) + '%\n')
            else:
                file.write('Adult content: ' +
                        str(0) + '%\n')
            file.write('Amount of scenes: ' + str(sceneCount) + '\n')

        with open(route + 'scenes.txt', 'a', 1) as file:
            file.write('Process time:\n')
            file.write('- Extraction: ' + str(timeProcesses['Extraction']) + '\n')
            file.write('- Analysis: ' + str(timeProcesses['Analysis']) + '\n')
        

        genders = ['Female', 'Male']
        colors = ['orange', 'green']
        gap = (0, 0.1)
        pyplot.pie(gender, labels=genders, autopct="%0.1f %%",
                   shadow=True, pctdistance=0.5, colors=colors, explode=gap)
        pyplot.title(label='Video: ' + video)
        pyplot.annotate(
            (
                '* Results:' +
                '\n  - Female: ' + str(gender[0]) +
                '\n  - Male: ' + str(gender[1])
            ), xy=(10, 20), xycoords='figure pixels')
        pyplot.savefig(route + 'gender.jpg')
        pyplot.close()
        tags = ['anger', 'contempt', 'disgust', 'fear',
                'happiness', 'neutral', 'sadness', 'surprise']
        pyplot.figure(figsize=(11, 6))
        pyplot.barh(tags, emotions)
        pyplot.title(label='Video: ' + video + '\nFrecuency')
        pyplot.ylabel('Emotions')
        pyplot.xlabel('Quantity')
        pyplot.annotate(
            ('* Results:' +
             '\n  - Number of faces: ' + str(faceCount)), xy=(8, 20), xycoords='figure pixels')
        pyplot.savefig(route + 'emotions.jpg')
        pyplot.close()
        score = ['positive', 'neutral', 'negative']
        pyplot.figure(figsize=(8, 5))
        pyplot.barh(score, audioScore)
        pyplot.title(label='Video: ' + video + '\nFrecuency')
        pyplot.ylabel('Feeling')
        pyplot.xlabel('Quantity')
        pyplot.savefig(route + 'feeling.jpg')
        pyplot.close()

'''
    Método principal, donde se crea el directorio y se hace
    el llamado correspondiente.
'''
def main(route):
    print('Welcome to the analyzer!')
    folderPath =  route
    nameVideos = os.listdir(folderPath)
    for video in nameVideos:
        createMovieDirectories(video.replace('.mp4', ''))
    extraction(nameVideos, folderPath)
    distribution(nameVideos)
    results(nameVideos)

if __name__ == "__main__":
    main('.\\videos')  # Address of the folder to analyze
