import requests;
import time;
import json;
import urllib;
import urllib2;
import calendar;

class Tinder:
    
    credentialFileName = None;
    facebookToken = None;
    facebookID = None;
    tinderToken = None;

    session = None;
    headers = None;

    def __init__(self, fileName="credentials.json"):
        self.credentialFileName = fileName;
        self.facebookID, self.facebookToken, self.tinderToken, lastUpdated = self.getTokensFromFile();
        self.session = requests.session();
        self.headers = self.generateHeaders();

        #If we don't have a Tinder token
        if len(self.tinderToken) == 0:
            self.login();
        
        #If our tindertoken is expired
        elif lastUpdated > 60 * 60 + int(time.time()):
            self.login();

        #Valid token
        else:
            print("Found Tinder Token: " + self.tinderToken);

    def getTokensFromFile(self):
        with open(self.credentialFileName) as credentials:
            data = json.load(credentials);
            facebookID = data["facebook_id"];
            facebookToken = data["facebook_token"];
            tinderToken = data["tinder_token"];
            lastUpdated = data["last_updated"];
            return (facebookID, facebookToken, tinderToken, lastUpdated);

    def saveTokensToFile(self):
        
        data = {
            "facebook_id": self.facebookID,
            "facebook_token": self.facebookToken,
            "tinder_token": self.tinderToken,
            "last_updated": int(time.time())
        };

        with open(self.credentialFileName, 'w') as credentials:
            json.dump(data, credentials);
            

    def login(self):
        payload = { 
            "force_refresh": "false",
            "locale": "en-US",
            "facebook_id": self.facebookID,
            "facebook_token": self.facebookToken
        };
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
            "If-None-Match": "2020547529",
            "Connection": "keep-alive",
            "os_version": "900002",
            "Content-Type": "application/json"
        };

        url = "https://api.gotinder.com/auth";
        result = self.session.post(url, data=json.dumps(payload), headers=headers, proxies=None);

        if result.status_code == 200:
            result = result.json();
            headers["X-Auth-Token"] = self.tinderToken;
            self.tinderToken = result["token"];
            self.headers = headers;
            self.session.headers.update(headers);
            print("Successful login with Tinder Token: " + self.tinderToken);
            self.saveTokensToFile();
        else:
            print("Unsuccessful login");
            print(json.dumps(result, indent=4));
            raise errors.RequestError("Couldn't authenticate");
        

    def generateHeaders(self):
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
            "If-None-Match": "2020547529",
            "Connection": "keep-alive",
            "os_version": "900002",
            "Content-Type": "application/json charset=utf-8"
        };
        return headers;



