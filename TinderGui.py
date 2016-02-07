import sys;
import urllib;
import json;
import cv2;
import numpy
from PIL import Image

from PyQt4 import QtGui, QtCore

from Tinder import Tinder;
from Person import Person;

class TinderGui(QtGui.QWidget):

    tinder = None;
    recommendations = None;

    swipeRightButton = None;
    swipeLeftButton = None;
    superLikeButton = None;

    currentImageLabel = None;
    personDescriptionTextEdit = None;

    photoIndex = None;

    rejectCounter = None;
    likeCounter = None;
    superLikeCounter = None;
    likesRemainingCounter = None;
    superLikesRemainingCounter = None;

    swipeInformationTextEdit = None;

    eyeColorLabel = None;
    eyeColorComboBox = None;

    hairColorLabel = None;
    hairColorComboBox = None;



    ###########################################################
    #                                                         #
    #               UI + GLOBAL VARIABLE SET UP               #
    #                                                         #  
    ###########################################################

    def __init__(self):
        super(TinderGui, self).__init__();

        self.photoIndex = 0;
        self.rejectCounter = 0;
        self.likeCounter = 0;
        self.superLikeCounter = 0;
        self.likesRemainingCounter = 50;
        self.superLikesRemainingCounter = 3;

        self.tinder = Tinder(fileName="credentials.json");
        self.recommendations = self.tinder.getRecommendations();

        if len(self.recommendations) == 0:
            print("0 RECOMMENDATIONS")
            return;

        self.initUI();

    def initUI(self):

        self.createUIComponents();
        self.displayPhoto();
        self.displayInformation();

        buttonSection = QtGui.QSplitter(QtCore.Qt.Horizontal)
        buttonSection.addWidget(self.swipeLeftButton);
        buttonSection.addWidget(self.swipeRightButton);
        buttonSection.addWidget(self.superLikeButton);

        middleSection = QtGui.QSplitter(QtCore.Qt.Vertical)
        middleSection.addWidget(self.currentImageLabel);
        middleSection.addWidget(buttonSection);

        eyeColorSection = QtGui.QSplitter(Qt.Horizontal);
        eyeColorSection.addWidget(self.eyeColorLabel);
        eyeColorSection.addWidget(self.eyeColorComboBox);

        hairColorSection = QtGui.QSplitter(Qt.Horizontal);
        hairColorSection.addWidget(self.hairColorLabel);
        hairColorSection.addWidget(self.hairColorComboBox);

        rightSection = QtGui.QSplitter(QtCore.Qt.Vertical);
        rightSection.addWidget(self.swipeInformationTextEdit);
        rightSection.addWidget(eyeColorSection);

        mainLayout = QtGui.QSplitter(QtCore.Qt.Horizontal)
        mainLayout.addWidget(self.personDescriptionTextEdit);
        mainLayout.addWidget(middleSection);
        mainLayout.addWidget(rightSection);
        mainLayout.adjustSize();

        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(mainLayout)
        self.setLayout(vbox)

        self.setWindowTitle('Tinder Bot');
        self.setWindowIcon(QtGui.QIcon('tinder_icon.png'));

        self.resize(1000, 800);
        self.center();
        self.show()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        

    def displayPhoto(self):
        url = self.recommendations[0].photos[self.photoIndex];
        data = urllib.urlopen(url).read();

        openCVImage  = self.handleFacialRecognition(data);

        #image = QtGui.QImage()
        #image.loadFromData(data)

        self.currentImageLabel.setPixmap(openCVImage);

    def displayInformation(self):
        person = self.recommendations[0];

        result = person.getName() + "\n\n" + person.getBirthDate() + "\n\n" + person.getDistance() + " Miles" + "\n\n" + person.getBio() + "\n\n" + person.getCommonConnections() + "\n\n" + person.getCommonInterests() + "\n\n" + person.getCommonLikes() + "\n\n" + person.getCommonFriends() + "\n\n" + person.getSchools() + "\n\n" + person.getJobs();
        self.personDescriptionTextEdit.setText(result);

    def createUIComponents(self):
        self.currentImageLabel = QtGui.QLabel(self)

        self.swipeRightButton = QtGui.QPushButton('Like', self);
        self.swipeLeftButton = QtGui.QPushButton('Pass', self);
        self.superLikeButton = QtGui.QPushButton('Super-Like', self);

        self.swipeRightButton.clicked.connect(self.swipeRight);
        self.swipeLeftButton.clicked.connect(self.swipeLeft);
        self.superLikeButton.clicked.connect(self.superLike);

        self.personDescriptionTextEdit = QtGui.QTextEdit();
        self.personDescriptionTextEdit.setEnabled(False);

        self.swipeInformationTextEdit = QtGui.QTextEdit();
        self.swipeInformationTextEdit.setEnabled(False);

        self.eyeColorLabel = QtGui.QLabel(self);
        self.eyeColorLabel.setText("Eye Color: ");
        self.eyeColorComboBox = QtGui.QComboBox(self);
        self.eyeColorComboBox.activated[str].connect(self.changedEyeColor);
        self.addEyeColorOptions();

        self.hairColorLabel = QtGui.QLabel(self);
        self.hairColorLabel.setText("Hair Color: ");
        self.hairColorComboBox = QtGui.QComboBox(self);
        self.hairColorComboBox.activated[str].connect(self.changedHairColor);
        self.addHairColorOptions();

    def displaySwipeInformation(self):
        result = "Rejected: " + str(self.rejectCounter) + "\n\n" + \
                "Liked: " + str(self.likeCounter) + "\n\n" + \
                "Likes Remaining: " + str(self.likesRemainingCounter) + "\n\n" + \
                "Super Liked: " + str(self.superLikeCounter) + "\n\n" + \
                "Super Likes Remaining: " + str(self.superLikesRemainingCounter);
        self.swipeInformationTextEdit.setText(result);

    def addEyeColorOptions(self):
        self.eyeColorComboBox.addItem("Brown");
        self.eyeColorComboBox.addItem("Blue");
        self.eyeColorComboBox.addItem("Green");

    def addHairColorOptions(self):
        self.hairColorComboBox.addItem("Black");
        self.hairColorComboBox.addItem("Brown");
        self.hairColorComboBox.addItem("Blonde");
        self.hairColorComboBox.addItem("Red");


    ###########################################################
    #                                                         #
    #               LISTENERS                                 #
    #                                                         #  
    ###########################################################

    def keyPressEvent(self, eventQKeyEvent):
        QtGui.QWidget.keyPressEvent(self, eventQKeyEvent)

        key = eventQKeyEvent.key();

        if key == QtCore.Qt.Key_Left:
            self.swipeLeft();
        elif key == QtCore.Qt.Key_Right:
            self.swipeRight();
        elif key == QtCore.Qt.Key_S:
            self.superLike();

        elif key == QtCore.Qt.Key_Up:
            self.photoIndex -= 1;
            if self.photoIndex < 0:
                self.photoIndex = len(self.recommendations[0].photos) - 1;
            self.displayPhoto();

        elif key == QtCore.Qt.Key_Down:
            self.photoIndex += 1;
            if self.photoIndex >= len(self.recommendations[0].photos):
                self.photoIndex = 0;
            self.displayPhoto();

    def handleSwipe(self):
        if len(self.recommendations) == 1:
            self.recommendations = self.tinder.getRecommendations();
        else:
            self.recommendations = self.recommendations[1:];
        self.displayPhoto();
        self.displayInformation();
        self.displaySwipeInformation();

    def superLike(self):
        success, result = self.tinder.superLike(self.recommendations[0].personID);

        if success:
            result = result["super_likes"];
            self.superLikesRemainingCounter = result["remaining"];
            self.superLikeCounter += 1;
            self.handleSwipe();
        else:
            QtGui.QMessageBox.about(self, "Error super liking person", json.dumps(result,indent=4));

    def swipeRight(self):
        success, result = self.tinder.swipeRight(self.recommendations[0].personID);

        if success:
            self.likesRemainingCounter = result["likes_remaining"];
            self.likeCounter += 1;
            self.handleSwipe();
        else:
            QtGui.QMessageBox.about(self, "Error liking person", json.dumps(result,indent=4));

    def swipeLeft(self):
        success, result = self.tinder.swipeLeft(self.recommendations[0].personID);

        if success:
            self.rejectCounter += 1;
            self.handleSwipe();
        else:
            QtGui.QMessageBox.about(self, "Error swiping left", json.dumps(result,indent=4));


    def changedEyeColor(self, text):
        print("Changed to: " + text);

    def changedHairColor(self):
        print("Changed to: " + text);

    def handleFacialRecognition(self, imageData):
        imageName = 'picture.png'
        cascPath = 'haarcascade_frontalface_default.xml'

        faceCascade = cv2.CascadeClassifier(cascPath)
        image = numpy.asarray(bytearray(imageData), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        #Scale factor = 1.1 b/c faces closer to camera are bigger than ones in back
        faces = faceCascade.detectMultiScale(image, scaleFactor=1.4, minNeighbors=1, minSize=(80,80), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)

        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imwrite(imageName, image);


        return QtGui.QPixmap(imageName);


    '''
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()        
    '''


def main():
    app = QtGui.QApplication(sys.argv);
    tinderGui = TinderGui();
    sys.exit(app.exec_());


if __name__ == '__main__':
    main();
   
