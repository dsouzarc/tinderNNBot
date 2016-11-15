from Person import Person

import requests;
import time;
import json;
import sys;

class Tinder:

    '''
    Handles all Tinder API calls 
    Loads credential information from "credentials.json"
    If the tokens are expired or missing, calls the API to renew the token
    '''

    credentialFileName = None;
    facebookToken = None;
    facebookID = None;
    tinderToken = None;
    tinderAPIToken = None;
    myName = None;

    session = None;
    headers = None;

    errorCount = 0;


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
            self.headers["Authorization"] = 'Token token=' + self.tinderToken + ''
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
            print("Like recorded \t" + str(result.json()))
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
            print("Super-like recorded \t" + str(result.json()))
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
        url = "https://api.gotinder.com/recs/core?locale=en-US";

        result = self.session.get(url,headers=self.headers, proxies=None);

        if result.status_code == 200:
            try:
                result = result.json();
                if result["status"] == 200:

                    #The people to swipe
                    results = result["results"]
                    for resultPerson in results:
                        if resultPerson["type"] == "user":
                            actualPerson = resultPerson["user"]
                            recommendation = Person(actualPerson);
                            recommendations.append(recommendation);
                    return recommendations

            except TypeError:
                print("NON-JSON RESPONSE - Might be login issue")
                print(result.text)

        #Error logging in or no recommendations
        elif result.status_code == 401 or len(recommendations) == 0:

            print("RESPONSE: " + result.text)
            self.errorCount += 1;

            #Give up
            if self.errorCount > 5:
                if result.status_code == 401:
                    print("Too many login errors - quitting now")
                else:
                    print("Too many no recommendations - quitting now")
                sys.exit();

            else:
                if result.status_code == 401:
                    print("Login error - trying again")
                else:
                    print("No recommendations - trying again")

                #Recurse until we should give up
                return self.getRecommendations();

        #Got our recommendations
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
            "app-version": "1798",
            "x-client-version": "65010",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US;q=1",
            "platform": "ios",
            "Facebook-ID": self.facebookID,
            "User-Agent": "Tinder/6.5.0 (iPhone; iOS 10.1; Scale/2.00)",
            "If-None-Match": 'W/"-330160069"',
            "Connection": "keep-alive",
            "os_version": "1000001",
            "Content-Type": "application/json"
        };

        url = "https://api.gotinder.com/auth";
        result = self.session.post(url, data=json.dumps(payload), headers=headers, proxies=None);

        if result.status_code == 200:
            result = result.json();
            self.tinderToken = result["token"];
            self.tinderAPIToken = result["user"]["api_token"];
            self.myName = result["user"]["full_name"];

            headers["X-Auth-Token"] = self.tinderToken;
            headers["Authorization"] = 'Token token=' + self.tinderToken  

            self.headers = headers;
            self.session.headers.update(self.headers);

            print("Successful logged " + self.myName + " in with Tinder Token: " + self.tinderToken + "\tAPI Token: " + self.tinderAPIToken);
            self.saveTokensToFile();
        
        elif result.status_code == 401:
            print("INVALID USERNAME/PASSWORD - 401 Error Code");
            print(result.text);

        else:
            print("Unsuccessful login");

            try:
                print(json.dumps(result, indent=4));
            except TypeError:
                print(result.text);
            raise errors.RequestError("Couldn't authenticate");
        

    '''
    The headers used
    '''
    def generateHeaders(self):
        headers = {
            "Host": "api.gotinder.com",
            "Accept": "*/*",
            "app-version": "1798",
            "x-client-version": "65010",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US;q=1",
            "platform": "ios",
            "Facebook-ID": self.facebookID,
            "User-Agent": "Tinder/6.5.0 (iPhone; iOS 10.1; Scale/2.00)",
            "If-None-Match": 'W/"-330160069"',
            "Connection": "keep-alive",
            "os_version": "1000001",
            "Content-Type": "application/json"
        };
        return headers;

    def getMatches(self):
        matchesURL = "https://api.gotinder.com/updates"
        result = self.session.post(matchesURL, headers=self.headers, proxies=None)
        result = result.json()
        matches = result["matches"]
        people = []
        for match in matches:
            if "person" in match:
                person = Person(match["person"])
                personInformationURL = "https://api.gotinder.com/user/" + person.personID
                personResult = self.session.get(personInformationURL, headers=self.headers, proxies=None).json()

                personResult = personResult["results"]
                person = Person(personResult)
                people.append(person)
                print(person.name + "\t" + person.getSchools())


if __name__ == "__main__":
    tinder = Tinder(fileName="credentials.json")
    recs = tinder.getRecommendations()
