from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

KEYS = ['', '']
ENDPOINTS = ['', '']


def textAnalyticsKey(pos):
    azureKey = AzureKeyCredential(KEYS[pos])
    azureTextAnalytics = TextAnalyticsClient(
        endpoint=ENDPOINTS[pos],
        credential=azureKey)
    return azureTextAnalytics
