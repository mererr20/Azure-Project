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
from audio import SplitWavAudioMubin
import time

BAD_WORDS = ["vodka"]

#API FACE
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

#COMPUTER VISION
subscription_key, endpoint = cnfg.config_computer_vision()
analyze_url = endpoint + "vision/v3.1/analyze"
headersVision = {'Ocp-Apim-Subscription-Key': subscription_key}
paramsVision = {'visualFeatures': 'Categories,Description'}

#SPEECH
subscription_key_audio, region = cnfg.config_audio()


# {'Peli':[]}
textAnalysis = []
sceneAnalysis = []
emotionAnalysis = []


def audio_to_text(audio):
    all_text = []
    done = False

    speech_config = speechsdk.SpeechConfig(subscription=subscription_key_audio, region=region)
    audio_config = speechsdk.audio.AudioConfig(filename=(audio))
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True
        
    # Connect callbacks to the events fired by the speech recognizer
    #speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt.result.text)))
    speech_recognizer.recognized.connect(lambda evt: all_text.append(evt.result.text))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    # Conver list to string
    text_complete=""
    for text in all_text:
        text_complete+=text
        text_complete+=" "
    return text_complete
    #audio_analysis(text_complete)

def audio_analysis(text):
    # Analyze words
    for word in BAD_WORDS:
        if word.lower() in text:
            print("{} es una mala palabra.".format(word.lower()))




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


def apiFace(image):
    image_data = open(image, "rb")
    response = requests.post(face_api_url, params=paramsFace,
                             headers=headersFace, data=image_data)
    response.raise_for_status()
    face = response.json()
    if face != []:
        return(face[0])
    return ''


def computerVision(image):
    data = {'url': image}
    response = requests.post(analyze_url, headers=headersVision,
                             params=paramsVision, json=data)

    analysis = response.json()
    return analysis


def azure(image):
    results = []
    results.append(apiFace(image))
    results.append(computerVision(image))
    results.append(image)
    print(results)
    return results


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
        textAnalysis.append({video:[textDetections]})

    print('\n\n')
    print(emotionAnalysis)
    print('\n\n')
    print(sceneAnalysis)
    print('\n\n')
    print(textAnalysis)


def audioExtraction(path, videoName):
    print("Converting...")
    video = mp.VideoFileClip((path + '\\' + videoName + '.mp4'))
    video.audio.write_audiofile(
        ('Data\\' + videoName + '\\temp\\' + videoName + '.wav'))


def audioSplit(videoName):
    audio = SplitWavAudioMubin(
        ('Data\\' + videoName + '\\temp'), (videoName + '.wav'))
    audio.multipleSplit(15)


def frameExtraction(videoName, video, start, end):
    while(start <= end):
        video.set(cv2.CAP_PROP_POS_MSEC, start)
        ret, frame = video.read()
        newRoute = '.\\Data\\' + videoName + '\\frames\\' + \
            str(start) + '_' + videoName + '.jpg'
        cv2.imwrite(newRoute, frame)
        cv2.waitKey(0)
        start += 5000
    video.release()
    cv2.destroyAllWindows()


def frames(path, videoName):
    video1 = cv2.VideoCapture((path + '\\' + videoName + '.mp4'))
    frames = video1.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = int(video1.get(cv2.CAP_PROP_FPS))
    seconds = int(frames / fps)
    miliseconds = int(seconds*1000)
    half = miliseconds/2
    video2 = cv2.VideoCapture((path + '\\' + videoName + '.mp4'))
    video1Thread = threading.Thread(
        target=frameExtraction, args=(videoName, video1, 0, half))
    video2Thread = threading.Thread(target=frameExtraction, args=(
        videoName, video2, half, miliseconds))
    video1Thread.start()
    video2Thread.start()
    video1Thread.join()
    video2Thread.join()


def startExtraction(path, video):
    audioExtraction(path, video)
    audioSplit(video)
    frames(path, video)


def main(videoFolderPath):
    videos = os.listdir(videoFolderPath)
    startTime = datetime.datetime.now()
    '''with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futureVideo = {executor.submit(startExtraction, videoFolderPath, video.replace(
            '.mp4', '')): createMovieDirectories(video.replace('.mp4', '')) for video in videos}
        for future in concurrent.futures.as_completed(futureVideo):
            try:
                print(future.result())
            except Exception as exc:
                print('%r generated an exception: %s' % (future, exc))'''
    analyzer(videos)
    endTime = datetime.datetime.now()
    print('Duration: {}'.format(endTime - startTime))


if __name__ == "__main__":
    # main('.\\videos')
    main('D:\\Peliculas')
