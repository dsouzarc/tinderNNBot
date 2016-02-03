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
    personDescriptionTextEdit = None;
    photoIndex = None;
    currentImageLabel = None;

    def __init__(self):
        super(TinderGui, self).__init__();

        self.photoIndex = 0;
        self.tinder = Tinder(fileName="credentials.json");
        self.recommendations = self.tinder.getRecommendations();

        if len(self.recommendations) == 0:
            print("0 RECOMMENDATIONS")
            return;

        self.initUI();

    def initUI(self):

        self.createUIComponents();
        self.displayPhoto();

        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addStretch(1)
        
        mainSplit = QtGui.QSplitter(QtCore.Qt.Vertical);
        mainSplit.addWidget(self.swipeLeftButton);
        mainSplit.addWidget(self.swipeRightButton);
        mainSplit.addWidget(self.personDescriptionTextEdit);

        imageSplit = QtGui.QSplitter(QtCore.Qt.Horizontal);
        imageSplit.addWidget(mainSplit);
        imageSplit.addWidget(self.currentImageLabel);

        mainLayout.addWidget(imageSplit);
        self.setLayout(mainLayout)

        self.setWindowTitle('Tinder Bot');
        self.setWindowIcon(QtGui.QIcon('tinder_icon.png'));

        self.resize(800, 800);
        self.center();
        self.show()
        
    def keyPressEvent (self, eventQKeyEvent):
        QtGui.QWidget.keyPressEvent(self, eventQKeyEvent)

        key = eventQKeyEvent.key();

        if key == QtCore.Qt.Key_Left:
            self.swipeLeft();
        elif key == QtCore.Qt.Key_Right:
            self.swipeRight();

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

    def createUIComponents(self):
        self.currentImageLabel = QtGui.QLabel(self)

        self.swipeRightButton = QtGui.QPushButton('Like', self);
        self.swipeLeftButton = QtGui.QPushButton('Pass', self);

        self.swipeRightButton.clicked.connect(self.swipeRight);
        self.swipeLeftButton.clicked.connect(self.swipeLeft);

        text = "";
        for i in range(0, 300):
            text += str(i)

        self.personDescriptionTextEdit = QtGui.QTextEdit();
        self.personDescriptionTextEdit.setText(text);
        self.personDescriptionTextEdit.setEnabled(False);


    def swipeRight(self):
        self.tinder.swipeRight(self.recommendations[0].personID);
        self.handleSwipe();

    def swipeLeft(self):
        self.tinder.swipeLeft(self.recommendations[0].personID);
        self.handleSwipe();

    def handleSwipe(self):
        if len(self.recommendations) == 1:
            self.recommendations = self.tinder.getRecommendations();
        else:
            self.recommendations = self.recommendations[1:];
        self.displayPhoto();


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
   
