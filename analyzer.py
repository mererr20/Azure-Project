import os
import requests
import AzureConfig as cnfg
import concurrent.futures
import azure.cognitiveservices.speech as speechsdk
import time


'''
'''


def apiFace(image, pos):
    time.sleep(0.5)
    # API FACE
    # Get the Face API keys
    subscriptionKeyFace, faceApiUrl = cnfg.configFace(pos)

    # Build headers and params to do the request.
    headersFace = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscriptionKeyFace
    }

    paramsFace = {
        'returnFaceId': 'false',
        'returnFaceAttributes': 'age,gender,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,exposure,noise'
    }

    imageData = open(image, "rb")
    response = requests.post(faceApiUrl, params=paramsFace,
                             headers=headersFace, data=imageData)
    response.raise_for_status()
    face = response.json()
    if face != []:
        return(face[0])
    return ''


'''
'''


def audioAnalysis(text):
    BADWORDS = ["vodka"]
    for word in BADWORDS:
        if word.lower() in text:
            print("{} es una mala palabra.".format(word.lower()))


def audioToText(audio, pos):

    # SPEECH
    subscriptionKeyAudio, region = cnfg.configAudio(pos)

    allText = []
    done = False
    speechConfig = speechsdk.SpeechConfig(
        subscription=subscriptionKeyAudio, region=region)
    audioConfig = speechsdk.audio.AudioConfig(filename=(audio))
    speechRecognizer = speechsdk.SpeechRecognizer(
        speech_config=speechConfig, audio_config=audioConfig)

    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        speechRecognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    # Connect callbacks to the events fired by the speech recognizer
    #speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt.result.text)))
    speechRecognizer.recognized.connect(
        lambda evt: allText.append(evt.result.text))
    speechRecognizer.session_started.connect(
        lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speechRecognizer.session_stopped.connect(
        lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speechRecognizer.canceled.connect(
        lambda evt: print('CANCELED {}'.format(evt)))

    # stop continuous recognition on either session stopped or canceled events
    speechRecognizer.session_stopped.connect(stop_cb)
    speechRecognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speechRecognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    # Conver list to string
    textComplete = ""
    for text in allText:
        textComplete += text
        textComplete += " "
    return textComplete
    #return audioAnalysis(textComplete)


'''
'''


def audioAnalyzer(video, pos):
    routeAudios = 'Data\\' + video + '\\audio'
    audios = os.listdir(routeAudios)
    textDetections = ['']
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_url = {executor.submit(
            audioToText, (routeAudios + '\\' + url), pos): url for url in audios}
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data = future.result()
                textDetections[0] = textDetections[0] + data
                # textDetections.append(data)
            except Exception as exc:
                print('%r generated an exception: %s' % (future, exc))
    return textDetections


'''
'''


def frameAnalyzer(video, pos):
    routeFrames = 'Data\\' + video + '\\frames'
    frames = os.listdir(routeFrames)
    emotionDetectionsFrame = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futureFrame = {executor.submit(
            apiFace, (routeFrames + '\\' + frame), pos): frame for frame in frames}
        for future in concurrent.futures.as_completed(futureFrame):
            try:
                data = future.result()
                emotionDetectionsFrame.append(data)
            except Exception as exc:
                print('%r generated an exception: %s' % (future, exc))
    return emotionDetectionsFrame
