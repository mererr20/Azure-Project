from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

KEYS = ['e05f24b6835c43a1bdc47bc056f808ce', '']
ENDPOINTS = ['https://cognitiveps.cognitiveservices.azure.com/', '']


def textAnalyticsKey(pos):
    azureKey = AzureKeyCredential(KEYS[pos])
    azureTextAnalytics = TextAnalyticsClient(
        endpoint=ENDPOINTS[pos],
        credential=azureKey)
    return azureTextAnalytics
