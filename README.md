#Written by Ryan D'souza

##A Tinder Bot - under construction

The bot analyzes the facial components of people you swipe for on Tinder so that it can automate the process and swipe for you.

OpenCV is used for facial recognition and identifying certain facial characteristics. Unfortunately, this does not work 100% of the time and some information must still be filled out manually.

The identified characteristics of both what you like (right swipe) and don't like (left swipe) are stored in a text file.
When the bot is in unsupervised mode, Google's TensorFlow library for machine learning is used to determine whether to autonomously swipe right or left for the potential match.
In both supervised and unsupervised mode, all of the potential matches' photos are analyzed. 

Uses PyQt for the GUI and Tinder's (unofficial) REST API. 


---
Though it is a boring/plain GUI, its main task is to train the neural net to on what the user likes and provide an interface for correcting the facial characteristics identified by OpenCV.

![Screenshot 0](https://github.com/dsouzarc/tinderAPI/blob/master/Screenshots/Screenshot_0.png)

![Screenshot 1](https://github.com/dsouzarc/tinderAPI/blob/master/Screenshots/Screenshot_1.png)
