subscription_key_face='98a37b7d054e43d99e5fa0a82eb7c94b'
face_api_key='https://cognitive-recognize.cognitiveservices.azure.com/face/v1.0/detect'
subscription_key_audio='ef8b2c96b20741e3a99f59962960ee91'
region='southcentralus'


def config_face():
    return subscription_key_face, face_api_key

def config_audio():
    return subscription_key_audio, region
