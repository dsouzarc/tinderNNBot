from Person import Person

import requests;
import time;
import json;

class Tinder:

    '''
    Handles all Tinder API calls 
    '''

    credentialFileName = None;
    facebookToken = None;
    facebookID = None;
    tinderToken = None;
    tinderAPIToken = None;
    myName = None;

    session = None;
    headers = None;


    '''
    Constructor 
    '''
    def __init__(self, fileName="credentials.json"):
        self.credentialFileName = fileName;
        self.facebookID, self.facebookToken, self.tinderToken, self.tinderAPIToken, self.myName, lastUpdated = self.getTokensFromFile();
        self.session = requests.session();
        self.headers = self.generateHeaders();

        #If we don't have a Tinder token
        if len(self.tinderToken) == 0 or len(self.tinderAPIToken) == 0:
            self.login();
        
        #If our tindertoken is expired
        elif int(time.time()) - lastUpdated > 60 * 60:
            self.login();

        #Valid token
        else:
            self.headers["X-Auth-Token"] = self.tinderToken;
            print(self.myName + " Found Tinder Token: " + self.tinderToken);


    '''
    Reads user credentials from file
    '''
    def getTokensFromFile(self):
        with open(self.credentialFileName) as credentials:
            data = json.load(credentials);
            facebookID = data["facebook_id"];
            facebookToken = data["facebook_token"];
            tinderToken = data["tinder_token"];
            tinderAPIToken = data["tinder_api_token"];
            myName = data["my_name"];
            lastUpdated = data["last_updated"];
            return (facebookID, facebookToken, tinderToken, tinderAPIToken, myName, lastUpdated);


    '''
    Saves the tokens to file
    '''
    def saveTokensToFile(self):
        data = {
            "facebook_id": self.facebookID,
            "facebook_token": self.facebookToken,
            "my_name": self.myName,
            "tinder_token": self.tinderToken,
            "tinder_api_token": self.tinderAPIToken,
            "last_updated": int(time.time())
        };

        with open(self.credentialFileName, 'w') as credentials:
            json.dump(data, credentials, indent=4, sort_keys=True);


    '''
    Swiping right - like
    '''
    def swipeRight(self, personId):
        url = "https://api.gotinder.com/like/" + personId + "?";
        result = self.session.get(url,headers=self.headers,proxies=None);

        if result.status_code == 200:
            print("Like recorded")
            return (True, result.json());
        else:
            print("ERROR LIKING PERSON: " + personId + "\t" + result.text);
            return (False, result.text);


    '''
    Super like
    '''
    def superLike(self, personId):
        url = "https://api.gotinder.com/like/" + personId + "/super/";
        result = self.session.post(url, headers=self.headers,proxies=None);

        if result.status_code == 200:
            result = result.json();
            if 'limit_exceeded' in result:
                if bool(result['limit_exceeded']):
                    return (False, result);
            print("Super-like recorded")
            return (True, result);

        else:
            print("ERROR SUPER LIKING PERSON: " + personId + "\t" + result.text)
            return (False, result.text);

    '''
    Swiping left - pass
    '''
    def swipeLeft(self, personId):
        url = "https://api.gotinder.com/pass/" + personId;
        result = self.session.get(url,headers=self.headers,proxies=None);

        if result.status_code == 200:
            print("Pass recorded")
            return (True, result.json())
        else:
            print("ERROR PASSING PERSON: " + personId + "\t" + result.text);
            return (False, result.text)


    '''
    Gets a list of people to swipe
    '''
    def getRecommendations(self):
        recommendations = [];
        url = "https://api.gotinder.com/user/recs?locale=en-US";
        result = self.session.post(url,headers=self.headers, proxies=None);

        if result.status_code == 200:
            result = result.json();
            if result["status"] == 200:
                for person in result["results"]:
                    recommendation = Person(person);
                    recommendations.append(recommendation);

        if len(recommendations) == 0:
            print("TRYING AGAIN 0 RECOMMENDATIONS: " + result.text);
            #self.login()
            return self.getRecommendations()
        else:
            return recommendations;


    '''
    Log in to Tinder API
    '''
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
            self.tinderAPIToken = result["user"]["api_token"];
            self.myName = result["user"]["full_name"];
            self.headers = headers;
            self.session.headers.update(headers);
            print("Successful logged " + self.myName + " in with Tinder Token: " + self.tinderToken + "\tAPI Token: " + self.tinderAPIToken);
            self.saveTokensToFile();
        else:
            print("Unsuccessful login");
            print(json.dumps(result, indent=4));
            raise errors.RequestError("Couldn't authenticate");
        

    '''
    The headers used
    '''
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
