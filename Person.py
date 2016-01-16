import json;

class Person:

    jsonData = None;
    name = None;
    photos = None;
    personID = None;
    swiped = None;

    def __init__(self, jsonData):
        
        self.jsonData = jsonData;
        self.name = jsonData["name"];
        self.personID = jsonData["_id"];
        self.photos = [];

        for photo in jsonData["photos"]:
            if "processedFiles" in photo:
                processedImages = photo["processedFiles"];
                for processedImage in processedImages:
                    if processedImage["width"] == 640 or processedImage["height"] == 640:
                        self.photos.append(processedImage["url"]);
            else:
                self.photos.append(photo['url']);

    def getPersonJSON():
        data = {
            "name": self.name,
            "photos" : self.photos,
            "personID" : self.personID,
            "data": self.jsonData
        };
        return data;

    def getCommonInterests():
        interests = [];
        for interest in self.jsonData["common_interests"]:
            interests.append(interest["name"]);
        return interests;

    def getInstagramPictures():
        pictures = [];
        if "instagram" in self.jsonData:
            instagram = self.jsonData["instagram"];

            if "completed_initial_fetch" in instagram and instagram["completed_initial_fetch"]:
                photos = instagram["photos"];
                for photo in photos:
                    pictures.append(photo["image"]);
        return pictures;
