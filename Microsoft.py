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

    session = None

    '''
    Constructor
    '''
    def __init__(self, fileName="credentials.json"):

        self.session = requests.session()
        self.credentials = json.load(open(fileName))


    def getEmotions(self, linkToImage):
        
        headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.credentials["microsoft_emotion_key1"]
        }

        body = {
            "url": linkToImage
        }

        url = "https://api.projectoxford.ai/emotion/v1.0/recognize"


        response = self.session.post(url, headers=headers, json=body)

        print(response.json())






microsoft = Microsoft(fileName="credentials.json")

microsoft.getEmotions("https://scontent-lga3-1.xx.fbcdn.net/t31.0-8/14876465_10210383671844847_1308604206555951240_o.jpg")



