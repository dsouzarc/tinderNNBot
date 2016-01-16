import requests;
import json;
import urllib;

class Tinder(Object):
    
    facebookID = None;
    tinderToken = None;

    session = None;
    headers = None;

    def __init__(self, facebookID, facebookToken):
        
        self.session = requests.session();
        self.facebookID = facebookID;

        self.headers = generateHeaders();

    def generateHeaders():
        headers = {
            "Host": "api.gotinder.com",
            "Accept": "*/*",
            "app-version": "467",
            "x-client-version": "47217",
            "Proxy-Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US;q=1",
            "platform": "ios",
            "Facebook-ID": self.facebookID,
            "User-Agent": "Tinder/4.7.2 (iPhone; iOS 9.2; Scale/2.00)",
            "If-None-Math": "\"2020547529\"",
            "Connection": "keep-alive",
            "os_version": "900002",
            "Content-Type": "application/json"
        };
        return headers;
