# Cognitive Recognize (Emotions) Config
subscription_key_face='98a37b7d054e43d99e5fa0a82eb7c94b'
face_api_key='https://cognitive-recognize.cognitiveservices.azure.com/face/v1.0/detect'

# Speech Config
subscription_key_audio='ef8b2c96b20741e3a99f59962960ee91'
region='southcentralus'

# Computer Vision Config
subscription_key_computer_vision = 'cb53891142e74441b616d26d8a7c60dc'
endpoint = 'https://computer-vision-so.cognitiveservices.azure.com/'


def config_face():
    return subscription_key_face, face_api_key

def config_audio():
    return subscription_key_audio, region

def config_computer_vision():
    return subscription_key_computer_vision, endpoint