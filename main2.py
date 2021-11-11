from math import inf
import os
import cv2
import datetime
import threading
import requests
import AzureConfig as cnfg
import moviepy.editor as mp
import concurrent.futures
import azure.cognitiveservices.speech as speechsdk
from audio import Audio
from frame import Frame
import math
import time

BAD_WORDS = ["vodka"]

# API FACE
# Get the Face API keys
subscription_key_face, face_api_url = cnfg.config_face()

# Build headers and params to do the request.
headersFace = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key_face
}

paramsFace = {
    'returnFaceId': 'false',
    'returnFaceAttributes': 'age,gender,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,exposure,noise'
}

# SPEECH
subscription_key_audio, region = cnfg.config_audio()


# {'Video':[]}
textAnalysis = []
sceneAnalysis = []
emotionAnalysis = []


def audio_to_text(audio):
    all_text = []
    done = False

    speech_config = speechsdk.SpeechConfig(
        subscription=subscription_key_audio, region=region)
    audio_config = speechsdk.audio.AudioConfig(filename=(audio))
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config)

    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    # Connect callbacks to the events fired by the speech recognizer
    #speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt.result.text)))
    speech_recognizer.recognized.connect(
        lambda evt: all_text.append(evt.result.text))
    speech_recognizer.session_started.connect(
        lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(
        lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(
        lambda evt: print('CANCELED {}'.format(evt)))

    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    # Conver list to string
    text_complete = ""
    for text in all_text:
        text_complete += text
        text_complete += " "
    return text_complete
    # audio_analysis(text_complete)


def audio_analysis(text):
    # Analyze words
    for word in BAD_WORDS:
        if word.lower() in text:
            print("{} es una mala palabra.".format(word.lower()))


def apiFace(image):
    image_data = open(image, "rb")
    response = requests.post(face_api_url, params=paramsFace,
                             headers=headersFace, data=image_data)
    response.raise_for_status()
    face = response.json()
    if face != []:
        return(face[0])
    return ''


def azure(image):
    results = []
    results.append(apiFace(image))
    results.append(image)
    print(results)
    return results


'''

'''
def frames(path, videoName):
    video = Frame(path, videoName)
    half = math.ceil(video.getMiliseconds() / 2)
    #video.thread(video.video1, 0, half)
    video.thread(video.video2, half, video.getMiliseconds())


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
def audio(path, videoName):
    audio = Audio(path, videoName)
    audio.audioExtraction()
    audio.setAudio()
    audio.multipleSplit(math.ceil(audio.getDurationMinutes()/4))


'''
    Este método llama a los demás métodos encargados de
    realizar la extracción del audio y frames de un video.
'''
def startExtraction(path, video):
    #audio(path, video)
    frames(path, video)
    return 'Extraction completed'


def extraction(videos, videoFolderPath):
    startTime = datetime.datetime.now()
    with concurrent.futures.ThreadPoolExecutor(max_workers = 3) as executor:
        futureVideo = {executor.submit(startExtraction, videoFolderPath, video.replace(
            '.mp4', '')): createMovieDirectories(video.replace('.mp4', '')) for video in videos}
        for future in concurrent.futures.as_completed(futureVideo):
            try:
                print(future.result())
            except Exception as exc:
                print('%r generated an exception: %s' % (future, exc))
    endTime = datetime.datetime.now()
    print('Time of the extraction method: {}'.format(endTime - startTime))


def analyzer(list):
    for video in list:
        video = video.replace('.mp4', '')
        routeFrames = 'Data\\' + video + '\\frames'
        routeAudios = 'Data\\' + video + '\\audio'
        frames = os.listdir(routeFrames)
        audios = os.listdir(routeAudios)
        emotionDetectionsFrame = []
        sceneDetectionsFrame = []
        '''with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            future_to_url = {executor.submit(
                azure, (routeFrames + '\\' + url)): url for url in frames}
            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    data = future.result()
                    emotionDetectionsFrame.append(data[0])
                    sceneDetectionsFrame.append(data[1])
                except Exception as exc:
                    print('%r generated an exception: %s' % (future, exc))'''

        textDetections = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            future_to_url = {executor.submit(
                audio_to_text, (routeAudios + '\\' + url)): url for url in audios}
            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    data = future.result()
                    textDetections.append(data)
                except Exception as exc:
                    print('%r generated an exception: %s' % (future, exc))

        emotionAnalysis.append({video: emotionDetectionsFrame})
        sceneAnalysis.append({video: sceneDetectionsFrame})
        textAnalysis.append({video: [textDetections]})

    print('\n\n')
    print(emotionAnalysis)
    print('\n\n')
    print(sceneAnalysis)
    print('\n\n')
    print(textAnalysis)


def results():
    print('')


if __name__ == "__main__":
    folderPath = '.\\videos'
    nameVideos = os.listdir(folderPath)
    extraction(nameVideos, folderPath)
    # analyzer(folderPath)
    # results()
