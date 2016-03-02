import json;
from dateutil.parser import parse
from datetime import datetime

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

    def getDataToSave(self):
        data = {
            "id": self.personID,
            "photos": self.photos,
            "name": self.name,
            "distance": self.getDistance(),
            "common_connections": self.getCommonConnections(),
            "schools": self.getSchools(),
            "jobs": self.getJobs(),
            "mutual_friends": self.getCommonFriends()
        }

        return data

    def getPersonJSON(self):
        data = {
            "name": self.name,
            "photos" : self.photos,
            "personID" : self.personID,
            "swiped": self.swiped,
            "data": self.jsonData
        };
        return data;

    def getInstagramPictures(self):
        pictures = [];
        if "instagram" in self.jsonData:
            instagram = self.jsonData["instagram"];

            if "completed_initial_fetch" in instagram and instagram["completed_initial_fetch"]:
                photos = instagram["photos"];
                for photo in photos:
                    pictures.append(photo["image"]);
        return pictures;

    def getName(self):
        return self.jsonData['name'];

    def getBio(self):
        return self.jsonData['bio'];

    def getBirthDate(self):
        dateString = self.jsonData['birth_date'];
        date = parse(dateString);
        result = str(date.month) + "/" + str(date.day) + "/" + str(date.year)
        return result;

    def isFemale(self):
        gender = int(self.jsonData['gender']);
        return gender == 1;

    def getGender(self):
        if self.isFemale():
            return "Female";
        else:
            return "Male";

    def getDistance(self):
        return str(self.jsonData['distance_mi']);

    def getCommonConnections(self):
        result = "";
        connections = self.jsonData['common_connections'];
        for connection in connections:
            result = connection['name'] + " " + result;
        return result;

    def getCommonInterests(self):
        result = "";
        interests = self.jsonData['common_interests'];
        for interest in interests:
            result = interest['name'] + " " + result;
        return result;

    def getCommonLikes(self):
        result = "";
        if 'common_likes' not in self.jsonData:
            print("NO COMMON LIKES: " + str(json.dumps(self.jsonData, indent=4)))
            return result;

        likes = self.jsonData['common_likes'];
        for like in likes:
            result = like['name'] + " " + result;
        return result;

    def getCommonFriends(self):
        result = "";

        if 'common_friends' not in self.jsonData:
            print("NO COMMON FRIENDS: " + str(json.dumps(self.jsonData, indent=4)))
            return result;

        friends = self.jsonData['common_friends'];
        for friend in friends:
            result = friend['name'] + " " + result;
        return result;

    def getSchools(self):
        result = "";
        schools = self.jsonData['schools'];
        for school in schools:
            result = school['name'] + " " + result;
        return result;

    def getJobs(self):
        result = "";
        jobs = self.jsonData['jobs'];
        for job in jobs:
            if 'title' in job:
                result += (job['title']['name'] + ", ");
            if 'company' in job:
                result = job['company']['name'] + " " + result;
        return result;
