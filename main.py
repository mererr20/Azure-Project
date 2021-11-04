from azure.cognitiveservices.vision.computervision.models import image_url
import cv2
import os
import json
import time
import glob
import torch
from PIL import Image
import multiprocessing
from matplotlib import pyplot

import requests
import AzureConfig as cnfg
import azure.cognitiveservices.speech as speechsdk
import moviepy.editor as mp

listMovies = any
BAD_WORDS = ["vodka"]

def cleanPath(route, movieDirectory):
    return str(movieDirectory).replace(route,'').replace('\\','').replace('.mp4','').replace(' ','').lower()

def getMoviesRoute(route):
    global listMovies
    listMovies = glob.glob(route + os.sep + '*.mp4')

def createDirectories(route):
    global listMovies
    for movieDirectory in listMovies:
        createMovieDirectories(cleanPath(route, movieDirectory))
        
def createMovieDirectories(nameMovie):
    try:
        if not os.path.exists('Frames'): 
            os.makedirs('Frames')
        if not os.path.exists('FinalResults'): 
            os.makedirs('FinalResults')
        if not os.path.exists('Frames\\' + nameMovie): 
            os.makedirs('Frames\\'+ nameMovie)
        if not os.path.exists('Frames\\' + nameMovie + '\\firstPortion'): 
            os.makedirs('Frames\\' + nameMovie + '\\firstPortion')
        if not os.path.exists('Frames\\' + nameMovie + '\\secondPortion'): 
            os.makedirs('Frames\\' + nameMovie + '\\secondPortion')
        if not os.path.exists('Frames\\' + nameMovie + '\\results'): 
            os.makedirs('Frames\\' + nameMovie + '\\results')
        open('Frames\\' + nameMovie + '\\results\\Person.txt',"w") 
        open('Frames\\' + nameMovie + '\\results\\Drink.txt',"w") 
        open('Frames\\' + nameMovie + '\\results\\Knife.txt',"w") 
        open('Frames\\' + nameMovie + '\\results\\Weapon.txt',"w")
        open('Frames\\' + nameMovie + '\\results\\Final.txt',"w")
    except OSError: 
        print ('Error: Creating directory of data')

def getFrames(route, list):
    print(list)
    for routeMovie in list:
        nameFolder = cleanPath(route, routeMovie)
        extractFrames(routeMovie, nameFolder)
  
def extractFrames(path, nameMovie):
    video = cv2.VideoCapture(path)
    sizeFrame = video.get(cv2.CAP_PROP_FRAME_COUNT)
    currentframe = 1
    count = 0
    timeRate = 1 # The time interval to capture video frames (here is a frame every 1 second)
    while(True): 
        ret,frame = video.read()
        FPS = video.get(5)
        if ret:
            frameRate = int (FPS) * timeRate
            if(currentframe % frameRate == 0 and currentframe < int(sizeFrame/2)): 
                name = './Frames/'+ nameMovie + '/firstPortion/frame' + str(count) + '.jpg'
                cv2.imwrite(name, frame)
                count += 1
            if(currentframe % frameRate == 0 and currentframe >= int(sizeFrame/2)):
                name = './Frames/'+ nameMovie + '/secondPortion/frame' + str(count) + '.jpg'
                cv2.imwrite(name, frame)
                count += 1
            currentframe += 1
            cv2.waitKey(0)
        else: 
            break
    video.release() 
    cv2.destroyAllWindows()

def getResultYOLO(route, list, folder):
    for movieDirectory in list:
        nameFolder = cleanPath(route, movieDirectory)
        root = '.\\Frames\\' + nameFolder + '\\'
        path =  root + folder
        listImage = glob.glob(path + os.sep + '*.jpg')
        inicio = time.time()
        for image in listImage:
            #yolo(root, image)
            azure_images(root, image)
        fin = time.time()
        writeTxt(root, 'Final', str(fin - inicio))
        
def writeTxt(path, className, data):
    route = path + 'results\\' + className + '.txt'
    with open(route, 'a', 1) as file:
        file.write(data + '\n')

def yolo(path, image):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=r'.\best.pt')
    model.conf = 0.25
    img = Image.open(image)
    results = model(img, size=640)
    className = results.pandas().xyxy[0].to_json()
    nameJSON = json.loads(className)["name"]
    for value in nameJSON.keys():
        writeTxt(path, nameJSON[value], '1')

def azure_images(path, image):
    # Get the Face API keys
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

def video_convert(video_name):
    print("Converting...")
    output_name = video_name.split(".mp4")[0]
    video = mp.VideoFileClip(str("videos/{}.mp4".format(video_name)))
    video.audio.write_audiofile("videos\{}.wav".format(output_name))
    audio_to_text("test3")

def audio_to_text(audio_name):
    subscription_key_audio, region = cnfg.config_audio()
    all_text = []
    done = False

    speech_config = speechsdk.SpeechConfig(subscription=subscription_key_audio, region=region)
    audio_config = speechsdk.audio.AudioConfig(filename="videos\{}.wav".format(audio_name))
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
    audio_analysis(text_complete)

def audio_analysis(text):
    # Analyze words
    for word in BAD_WORDS:
        if word.lower() in text:
            print("{} es una mala palabra.".format(word.lower()))

def computer_vision(image):
    subscription_key, endpoint = cnfg.config_computer_vision()
    analyze_url = endpoint + "vision/v3.1/analyze"

    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    params = {'visualFeatures': 'Categories,Description'}
    data = {'url': image}
    response = requests.post(analyze_url, headers=headers,
                            params=params, json=data)

    analysis = response.json()
    print(analysis)

def readTxt(path, className):
    route = path + 'results\\' + className + '.txt'
    count = 0
    with open(route, 'r', 1) as file:
        for line in file:
            try:
                if line != '\n':
                    count += int(line)
            except:
                count += float(line)
    with open(route, 'w', 1) as file:
        file.write(str(count))

def countResults(route):
    global listMovies
    for movieDirectory in listMovies:
        nameFolder = cleanPath(route, movieDirectory)
        root = '.\\Frames\\' + nameFolder + '\\'
        readTxt(root, 'Drink')
        readTxt(root, 'Final')
        readTxt(root, 'Knife')
        readTxt(root, 'Person')
        readTxt(root, 'Weapon')

def getLine(root):
    with open(root, 'r', 1) as file:
        for line in file:
            return line

def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)

def generateGraph(route):
    global listMovies
    classes = ('Person', 'Drink', 'Weapon', 'Knife')

    for movieDirectory in listMovies:
        nameFolder = cleanPath(route, movieDirectory)
        root = '.\\Frames\\' + nameFolder + '\\results\\'
        list = []
        list.append(int(getLine((root + 'Person.txt'))))
        list.append(int(getLine((root + 'Drink.txt'))))
        list.append(int(getLine((root + 'Weapon.txt'))))
        list.append(int(getLine((root + 'Knife.txt'))))

        slices = tuple(list)
        colores = ('#008F39','#7EBDC2','#DD98AA','#BB4430')
        pyplot.rcParams['toolbar']  = 'None'
        _,_,texto = pyplot.pie(slices, colors=colores, labels=classes, autopct='%1.1f%%')
        for tex in texto:
            tex.set_color('white')
        time = float(getLine((root + 'Final.txt')))

        pyplot.annotate(
            (
            '* Results:' +
            '\n  - Person: ' + str(list[0]) +
            '\n  - Drink: ' + str(list[1]) +
            '\n  - Weapon: ' + str(list[2]) +
            '\n  - Knife: ' + str(list[3]) +
            '\n* Time: ' + convert(time) + '.'
            ), xy=(10, 20), xycoords='figure pixels')
        pyplot.axis('equal')
        pyplot.title('Film: ' + nameFolder)
        pyplot.savefig('.\\FinalResults\\' + nameFolder + '.jpg')
        pyplot.close()

        print('In film ' + nameFolder + ', the following classes have been detected: ' +
                '\n\tPerson: ' + str(list[0]) +
                '\n\tDrink: ' + str(list[1]) +
                '\n\tWeapon: ' + str(list[2]) +
                '\n\tKnife: ' + str(list[3]) +
                '\nThis detection was carried out in ' + convert(time) + '.')

def firstProcesses(routeDirectory,mitad,size):
    global listMovies
    #Processes to get the frames of the videos
    if (size > 1):
        p1 = multiprocessing.Process(target=getFrames, args= (routeDirectory,listMovies[0:mitad]))
        p2 = multiprocessing.Process(target=getFrames, args= (routeDirectory,listMovies[mitad:size]))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
    else:
        p1 = multiprocessing.Process(target=getFrames, args= (routeDirectory,listMovies))
        p1.start()
        p1.join()

def secondProcesses(routeDirectory,mitad,size):
    global listMovies
    #Process to send the images to YOLO
    if (size > 1):
        p3 = multiprocessing.Process(target=getResultYOLO, args= (routeDirectory, listMovies[0:mitad], 'firstPortion'))
        p4 = multiprocessing.Process(target=getResultYOLO, args= (routeDirectory, listMovies[mitad:size],'secondPortion'))
        p5 = multiprocessing.Process(target=getResultYOLO, args= (routeDirectory, listMovies[0:mitad], 'firstPortion'))
        p6 = multiprocessing.Process(target=getResultYOLO, args= (routeDirectory, listMovies[mitad:size],'secondPortion'))
        p3.start()
        p4.start()
        p5.start()
        p6.start()
        p3.join()
        p4.join()
        p5.join()
        p6.join()
    else:
        p3 = multiprocessing.Process(target=getResultYOLO, args= (routeDirectory, listMovies, 'firstPortion'))
        p4 = multiprocessing.Process(target=getResultYOLO, args= (routeDirectory, listMovies,'secondPortion'))
        p3.start()
        p4.start()
        p3.join()
        p4.join()

def main(routeDirectory):
    global listMovies
    getMoviesRoute(routeDirectory)
    createDirectories(routeDirectory)
    size = len(listMovies)
    mitad = int(size/2)

    firstProcesses(routeDirectory,mitad,size)
    secondProcesses(routeDirectory,mitad,size)

    countResults(routeDirectory)
    generateGraph(routeDirectory)

'''if __name__ == "__main__":
    cpuCount = multiprocessing.cpu_count()
    if (cpuCount >= 4):
        print('Welcome to the movie analyzer!')
        main('.\\videos') #Address of the folder to analyze
    else:
        print("I'm really sorry, but your system doesn't meet the requirements...\n" +
        "You need at least 4 processors, and you have " + cpuCount)'''


#video_convert("test3")
url = 'https://www.gob.mx/cms/uploads/article/main_image/99875/WhatsApp_Image_2020-09-12_at_12.25.14.jpeg'
computer_vision(url)