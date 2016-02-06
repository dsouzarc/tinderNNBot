import sys;
import urllib;

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

        rightSection = QtGui.QSplitter(QtCore.Qt.Vertical);
        rightSection.addWidget(self.swipeInformationTextEdit);

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


    def displayPhoto(self):
        url = self.recommendations[0].photos[self.photoIndex];
        data = urllib.urlopen(url).read();

        image = QtGui.QImage()
        image.loadFromData(data)

        self.currentImageLabel.setPixmap(QtGui.QPixmap(image))

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

    def superLike(self):
        success, result = self.tinder.superLike(self.recommendations[0].personID);

        if success:
            result = result["super_likes"];
            self.superLikesRemainingCounter = result["remaining"];
            self.superLikeCounter += 1;
            self.handleSwipe();

    def swipeRight(self):
        success, result = self.tinder.swipeRight(self.recommendations[0].personID);

        if success:
            self.likesRemainingCounter = result["likes_remaining"];
            self.likeCounter += 1;
            self.handleSwipe();

    def swipeLeft(self):
        success, result = self.tinder.swipeLeft(self.recommendations[0].personID);

        if success:
            self.rejectCounter += 1;
            self.handleSwipe();

    def handleSwipe(self):
        if len(self.recommendations) == 1:
            self.recommendations = self.tinder.getRecommendations();
        else:
            self.recommendations = self.recommendations[1:];
        self.displayPhoto();
        self.displayInformation();
        self.displaySwipeInformation();


    def displaySwipeInformation(self):
        result = "Rejected: " + str(self.rejectCounter) + "\n\n" + \
                "Liked: " + str(self.likeCounter) + "\n\n" + \
                "Likes Remaining: " + str(self.likesRemainingCounter) + "\n\n" + \
                "Super Liked: " + str(self.superLikeCounter) + "\n\n" + \
                "Super Likes Remaining: " + str(self.superLikesRemainingCounter);
        self.swipeInformationTextEdit.setText(result);

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

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        

def main():
    app = QtGui.QApplication(sys.argv);
    tinderGui = TinderGui();
    sys.exit(app.exec_());


if __name__ == '__main__':
    main();
   
