import json

from pymongo import MongoClient

from Person import Person
from Microsoft import FacialEmotion


class MongoHandler:

    connection = None
    database = None

    rightSwipeCollection = None
    leftSwipeCollection = None


    def __init__(self):
        self.connection = MongoClient('localhost', 27017)
        self.database = self.connection['Tinder-database']

        self.rightSwipeCollection = self.database['right-swipes']
        self.leftSwipeCollection = self.database['left-swipe']


    def swipeRight(self, person, weight=1.0):
        dataToSave = person.getMongoDataToSave()
        dataToSave["weight"] = weight
        dataToSave["superlike"] = False

        try:
            result = self.rightSwipeCollection.insert(dataToSave)
        except Exception, e:
            print("Error saving right swipe: " + str(e))

    def superLike(self, person, weight=2.0):
        dataToSave = person.getMongoDataToSave()
        dateToSave["weight"] = weight
        dataToSave["superlike"] = True

        try:
            result = self.rightSwipeCollection.insert(dataToSave)
        except Exception, e:
            print("Error saving super like swipe: " + str(e))

    def swipeLeft(self, person, weight=1.0):
        dataToSave = person.getMongoDataToSave()
        dataToSave["weight"] = weight
        
        try:
            result = self.leftSwipeCollection.insert(dataToSave)
        except Exception, e:
            print("Error saving left swipe: " + str(e))


if __name__ == "__main__":
    mongo = MongoHandler()

