import requests
import json
import sys

class Microsoft:

    '''
    Handles API calls to Microsoft Cognitive Services API
    Ex. service: Facial and Emotion Detection
    '''

    #Dictionary of credentials
    credentials = None

    '''
    Constructor
    '''
    def __init__(self, fileName="credentials.json"):

        self.credentials = json.load(open(fileName))
        print(self.credentials["microsoft_emotion_key1"])

microsoft = Microsoft(fileName="credentials.json")



