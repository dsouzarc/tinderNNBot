import sys;
import urllib;
from PyQt4 import QtGui;

from Tinder import Tinder;
from Person import Person;


class TinderGui(QtGui.QWidget):

    tinder = None;

    swipeRightButton = None;
    swipeLeftButton = None;

    def __init__(self):
        super(TinderGui, self).__init__();

        self.tinder = Tinder(fileName="credentials.json");
        self.initUI();

    def initUI(self):

        self.swipeRightButton = QtGui.QPushButton('Right', self);
        self.swipeLeftButton = QtGui.QPushButton('Left', self);
        self.swipeRightButton.clicked.connect(self.swipeRight);
        self.swipeLeftButton.clicked.connect(self.swipeLeft);

        recommendations = self.tinder.getRecommendations();

        #url = recommendations[0].photos[0];
        url = "http://iconshow.me/media/images/ui/ios7-icons/png/512/person_1.png"
        data = urllib.urlopen(url).read();

        image = QtGui.QImage()
        image.loadFromData(data)

        lbl = QtGui.QLabel(self)
        lbl.setPixmap(QtGui.QPixmap(image))

        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addStretch(1)
        mainLayout.addWidget(self.swipeLeftButton);
        mainLayout.addWidget(self.swipeRightButton);

        mainLayout.addWidget(lbl)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        #vbox.addLayout(mainLayout)
        self.setLayout(mainLayout)

        self.setWindowTitle('Tinder Bot');
        self.setWindowIcon(QtGui.QIcon('tinder_icon.png'));
        self.resize(250, 150);
        self.center();
        self.show()

    def swipeRight(self):
        print("Swiped right");
    def swipeLeft(self):
        print("Swiped left");


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
   
