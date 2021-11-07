from math import inf
import os
from typing import Counter
import cv2
import datetime
import threading
import requests
import AzureConfig as cnfg
import moviepy.editor as mp
import concurrent.futures
from audio import SplitWavAudioMubin

info = []

#{'Peli':[]}
textAnalysis = []
sceneAnalysis = []
emotionAnalysis = []


def createMovieDirectories(nameMovie):
    try:
        if not os.path.exists('FinalResults'):
            os.makedirs('FinalResults')

        if not os.path.exists('Data'):
            os.makedirs('Data')

        if not os.path.exists('Data\\' + nameMovie):
            os.makedirs('Data\\' + nameMovie)

        if not os.path.exists('Data\\' + nameMovie + '\\frames'):
            os.makedirs('Data\\' + nameMovie + '\\frames')

        if not os.path.exists('Data\\' + nameMovie + '\\audio'):
            os.makedirs('Data\\' + nameMovie + '\\audio')

        if not os.path.exists('Data\\' + nameMovie + '\\temp'):
            os.makedirs('Data\\' + nameMovie + '\\temp')

    except OSError:
        print('Error: Creating directory of data')


def azure_images(image):
    '''# Get the Face API keys
    subscription_key_face, face_api_url = cnfg.config_face()

    # Build headers and params to do the request.
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key_face
    }
    
    params = {
        'returnFaceId': 'false',
        'returnFaceAttributes': 'age,gender,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,exposure,noise'
    }

    image_data = open(image, "rb")
    response = requests.post(face_api_url, params=params, headers=headers, data=image_data)
    response.raise_for_status()
    face = response.json()
    if face != []:
        print(image)
        print(face[0])
        print("\n")
        return(face[0])
    return '''
    return 'intento ' + image

'''def getDetectionsFrames(route, list, video):
    
    for nameFrame in list:
        print(nameFrame)
        emotiondetectionsFrame.append(azure_images((route + '\\' + nameFrame)))
    emotionAnalysis.append({video:emotiondetectionsFrame})
    return 'algo cax'''

def analyzer(list):

    for video in list:
        video = video.replace('.mp4', '')
        route = 'Data\\' + video + '\\frames'
        frames = os.listdir(route)
        emotiondetectionsFrame = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            future_to_url = {executor.submit(azure_images, (route + '\\' + url)): url for url in frames}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    emotiondetectionsFrame.append(future.result())
                except Exception as exc:
                    print('%r generated an exception: %s' % (url, exc))
        emotionAnalysis.append({video:emotiondetectionsFrame})

        '''start = 0
        quarter = int(len(frames)/4)
        end = quarter



        threadList = []

        for x in range(4):
            print()
            start += quarter
            end += quarter
            video_thread = threading.Thread(target=getDetectionsFrames, args=(route, frames[start:end], video))
            video_thread.start()
            threadList.append(video_thread)

        for video_thread in threadList:
            results = video_thread.join()
            print(results)'''
    print(emotionAnalysis)


def audioExtraction(path, videoName):
    print("Converting...")
    video = mp.VideoFileClip((path + '\\' + videoName + '.mp4'))
    video.audio.write_audiofile(
        ('Data\\' + videoName + '\\temp\\' + videoName + '.wav'))


def audioSplit(videoName):
    audio = SplitWavAudioMubin(
        ('Data\\' + videoName + '\\temp'), (videoName + '.wav'))
    audio.multipleSplit(1)


def frameExtraction(path, videoName):
    video = cv2.VideoCapture((path + '\\' + videoName + '.mp4'))
    currentframe = 1
    counter = 0
    # The time interval to capture video frames (here is a frame every 1 second)
    timeRate = 5
    while(True):
        ret, frame = video.read()
        FPS = video.get(5)
        if ret:
            frameRate = int(FPS) * timeRate
            if(currentframe % frameRate == 0 and currentframe):
                newRoute = '.\\Data\\' + videoName + '\\frames\\' + \
                    str(counter) + '_' + videoName + '.jpg'
                cv2.imwrite(newRoute, frame)
                counter += 1
            currentframe += 1
            cv2.waitKey(0)
        else:
            break
    video.release()
    cv2.destroyAllWindows()


def startExtraction(path, video):
    audioExtraction(path, video)
    audioSplit(video)
    frameExtraction(path, video)
    info.append('ALGO')


def main(videoFolderPath):
    threadList = []
    videos = os.listdir(videoFolderPath)
    start_time = datetime.datetime.now()
    '''for v in videos:
        video = v.replace('.mp4', '')
        createMovieDirectories(video)
        video_thread = threading.Thread(
            target=startExtraction, args=(videoFolderPath, video))
        video_thread.start()
        threadList.append(video_thread)
    for video_thread in threadList:
        video_thread.join()
    end_time = datetime.datetime.now()
    print('Duration: {}'.format(end_time - start_time))
    print(info)'''
       
    analyzer(videos)


if __name__ == "__main__":
    main('.\\videos')
