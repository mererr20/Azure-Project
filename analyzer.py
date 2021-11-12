import os
import AzureConfig as cnfg
import concurrent.futures

import time
import os.path
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

'''
'''


def computerVision(imagePath, pos):
    image = open(os.path.join(imagePath), "rb")
    azureComputerVision = ComputerVisionClient(
        cnfg.ENDPOINTS[pos], CognitiveServicesCredentials(cnfg.KEYS[pos]))
    sceneAttributes = ["adult", "description"]
    results = azureComputerVision.analyze_image_in_stream(
        image, sceneAttributes)
    if results:
        return results
    return ''


'''
'''


def apiFace(imagePath, pos):
    print(os.path.basename(imagePath))
    image = open(os.path.join(imagePath), "rb")
    apiFace = FaceClient(
        cnfg.ENDPOINTS[pos], CognitiveServicesCredentials(cnfg.KEYS[pos]))
    faceAttributes = ['age', 'gender', 'smile', 'facialHair',
                      'emotion', 'hair', 'accessories', 'noise']
    detected = apiFace.face.detect_with_stream(
        image=image, return_face_attributes=faceAttributes)
    if detected:
        return detected
    return ''


'''
'''


def audioToText(audio, pos):
    allText = []
    done = False
    speechConfig = speechsdk.SpeechConfig(
        subscription=cnfg.KEYS[pos], region='southcentralus')
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


'''
'''


def audioAnalyzer(video, pos):
    routeAudios = 'Data\\' + video + '\\audio'
    audios = os.listdir(routeAudios)
    textDetections = ['']
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futureAudio = {executor.submit(
            audioToText, (routeAudios + '\\' + audio), pos): audio for audio in audios}
        for future in concurrent.futures.as_completed(futureAudio):
            try:
                data = future.result()
                textDetections[0] = textDetections[0] + data
            except Exception as exc:
                print('%r generated an exception: %s' % (future, exc))
    print(textDetections)
    if textDetections[0] != '':
        azure = cnfg.textAnalyticsKey(pos)
        response = azure.analyze_sentiment(documents=textDetections)[0]
        return response
    return ''


def frameAnalyzer(imagePath, pos):
    results = []
    results.append(apiFace(imagePath, pos)[0])
    results.append(computerVision(imagePath, pos))
    return results


'''
'''


def frameDistribution(video, pos):
    routeFrames = 'Data\\' + video + '\\frames'
    frames = os.listdir(routeFrames)
    faceDetectionsFrame = []
    sceneDetectionsFrame = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futureFrame = {executor.submit(
            frameAnalyzer, (routeFrames + '\\' + frame), pos): frame for frame in frames}
        for future in concurrent.futures.as_completed(futureFrame):
            try:
                data = future.result()
                faceDetectionsFrame.append(data[0])
                sceneDetectionsFrame.append(data[1])
            except Exception as exc:
                print('%r generated an exception: %s' % (future, exc))
    return [faceDetectionsFrame, sceneDetectionsFrame]
