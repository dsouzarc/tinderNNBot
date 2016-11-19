import requests
import json
import sys

from PIL import Image, ImageDraw, ImageFont

class FacialEmotion:

    jsonResponse = None

    def __init__(self, jsonResponse):
        self.jsonResponse = jsonResponse

    def getDimensions(self):
        dim = self.jsonResponse["faceRectangle"]
        "Properties: height, left, top, width"
        return dim

    def getMainEmotion(self):
        emotions = self.jsonResponse["scores"]

        highestEmotion = emotions.keys()[0]
        highestScore = emotions[highestEmotion]

        for emotion in emotions.keys():
            if emotions[emotion] > highestScore:
                highestEmotion = emotion
                highestScore = emotions[emotion]

        return (highestEmotion, highestScore)

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
        response = self.session.post(url, headers=headers, json=body).json()

        facialEmotions = []

        if len(response) != 0:
            for face in response:
                f = FacialEmotion(face)
                facialEmotions.append(f)
                print(f.getDimensions())
                print(f.getMainEmotion())
            print("NOT 0")

        return facialEmotions




microsoft = Microsoft(fileName="credentials.json")

facialEmotions = microsoft.getEmotions("https://scontent-lga3-1.xx.fbcdn.net/t31.0-8/14876465_10210383671844847_1308604206555951240_o.jpg")


im = Image.open("/Users/Ryan/Downloads/14876465_10210383671844847_1308604206555951240_o.jpg")

draw = ImageDraw.Draw(im)

for facialEmotion in facialEmotions:
    face = facialEmotion.getDimensions()

    lineFill = 500
    lineWidth = 5

    faceX0 = face["left"]
    faceX1 = face["left"] + face["width"]
    faceY0 = face["top"]
    faceY1 = face["top"] + face["height"]

    #Left to right side of face, top 
    draw.line((faceX0, faceY0, faceX1, faceY0), width=lineWidth, fill=lineFill)

    #Left to right side of face, bottom 
    draw.line((faceX0, faceY1, faceX1, faceY1), width=lineWidth, fill=lineFill)

    #Left side of face, top to bottom
    draw.line((faceX0, faceY0, faceX0, faceY1), width=lineWidth, fill=lineFill)

    #Right side of face, top to bottom
    draw.line((faceX1, faceY0, faceX1, faceY1), width=lineWidth, fill=lineFill)

    mainEmotion = facialEmotion.getMainEmotion()
    draw.text((max(0, faceX0 - 60), max(0, faceY0 - 40)), mainEmotion[0], font=ImageFont.truetype("Verdana.ttf",34), fill=lineFill)


im.show()
