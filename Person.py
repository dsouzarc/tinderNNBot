import json;

class Person:

    jsonData = None;
    name = None;
    photos = None;
    personID = None;
    swiped = None; # -1 = No swipe, 0 = passed, 1 = like, 2 = super like

    def __init__(self, jsonData, personJSON=None):
        
        if personJSON is None:
            self.jsonData = jsonData;
            self.name = jsonData["name"];
            self.personID = jsonData["_id"];
            self.swiped = -1;
            self.photos = [];

            for photo in jsonData["photos"]:
                if "processedFiles" in photo:
                    processedImages = photo["processedFiles"];
                    for processedImage in processedImages:
                        if processedImage["width"] == 640 or processedImage["height"] == 640:
                            self.photos.append(processedImage["url"]);
                else:
                    self.photos.append(photo['url']);
        else:
            self.name = personJSON["name"];
            self.photos = personJSON["photos"];
            self.personID = personJSON["personID"];
            self.swiped = personJSON["swiped"];

    def getPersonJSON():
        data = {
            "name": self.name,
            "photos" : self.photos,
            "personID" : self.personID,
            "swiped": self.swiped,
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
