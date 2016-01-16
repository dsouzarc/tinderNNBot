from Tinder import Tinder;
from Person import Person;

tinder = Tinder(fileName="credentials.json");

recommendations = tinder.getRecommendations();

for person in recommendations:
    print person.name;

