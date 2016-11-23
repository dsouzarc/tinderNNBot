import requests
import json
import sys

from StringIO import StringIO
from PIL import Image, ImageDraw, ImageFont

######################################################################
#
#                   Facial Emotion - API return object
#                   
######################################################################


class FacialEmotion:

    '''
    Represents the object returned from an API call to Microsoft's Emotions API
    Includes the dimensions/coordinates of identified faces
    And the strengths of emotions for each face
    '''

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



######################################################################
#
#                   Microsoft - API Client
#                   
######################################################################


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


    '''
    Makes the API call to Microsoft's Emotions API
    Returns an array of FacialEmotion objects
    '''
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
        else:
            print("No faces in this image: " + linkToImage)

        return facialEmotions

    
    '''
    Responsible for drawing the rectangles around faces and emotions on an image
    If those values are not supplied, makes the appropriate calls to get them
    '''
    def drawFacesAndEmotions(self, pathToImage, image=None, facialEmotions=None):

        #If we aren't supplied an image, download it
        if image is None:
            image = Image.open(StringIO(requests.get(pathToImage).content))

        #If we aren't supplied the facial emotions, get it
        if facialEmotions is None:
            facialEmotions = self.getEmotions(pathToImage)

        #For drawing lines and text on the image
        draw = ImageDraw.Draw(image)

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

            #Draw the main emotion
            mainEmotion = facialEmotion.getMainEmotion()
            draw.text((max(0, faceX0 - 60), max(0, faceY0 - 40)), mainEmotion[0], font=ImageFont.truetype("Verdana.ttf",34), fill=lineFill)

        #Return our image with everything drawn
        return image



######################################################################
#
#                   Main method - testin
#                   
######################################################################

if __name__ == "__main__":

    microsoft = Microsoft(fileName="credentials.json")

    if len(sys.argv) > 1:
        url = sys.argv[1] #raw_input("Link to photo to analyze: ")
    else:
        url = "https://scontent-lga3-1.xx.fbcdn.net/t31.0-8/14876465_10210383671844847_1308604206555951240_o.jpg"

    image = microsoft.drawFacesAndEmotions(url)
    image.show()
