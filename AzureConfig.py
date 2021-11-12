# Cognitive Recognize (Emotions) Config
subscriptionKeyFace = ['98a37b7d054e43d99e5fa0a82eb7c94b', '86706fb9de4840aeb8ed83678f6bf9c0']
faceApiKey = ['https://cognitive-recognize.cognitiveservices.azure.com/face/v1.0/detect', 'https://cognitive-service-so.cognitiveservices.azure.com/face/v1.0/detect']


# Speech Config
subscriptionKeyAudio = ['ef8b2c96b20741e3a99f59962960ee91', '2fa1606fba5a4e0dab52263d50faaad5']
region = 'southcentralus'

def configFace(pos):
    return subscriptionKeyFace[pos], faceApiKey[pos]

def configAudio(pos):
    return subscriptionKeyAudio[pos], region