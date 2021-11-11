# Cognitive Recognize (Emotions) Config
subscription_key_face='98a37b7d054e43d99e5fa0a82eb7c94b'
face_api_key='https://cognitive-recognize.cognitiveservices.azure.com/face/v1.0/detect'

# Speech Config
subscription_key_audio='ef8b2c96b20741e3a99f59962960ee91'
region='southcentralus'

def config_face():
    return subscription_key_face, face_api_key

def config_audio():
    return subscription_key_audio, region


'''
Speech:
key1: 2fa1606fba5a4e0dab52263d50faaad5
endpoint: https://speech-so.cognitiveservices.azure.com/sts/v1.0/issuetoken

Face:
key1: 86706fb9de4840aeb8ed83678f6bf9c0
endpoint: https://cognitive-service-so.cognitiveservices.azure.com/
'''