import sys
from PyQt4 import QtGui

from Tinder import Tinder;
from Person import Person;


class TinderGui(QtGui.QWidget):

    def __init__(self):
        super(TinderGui, self).__init__();

        self.initUI();

    def initUI(self):
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        
        self.setToolTip('This is a <b>QWidget</b> widget')
        
        btn = QtGui.QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)       
        
        self.resize(250, 150);
        self.center();
        self.setWindowTitle('Tinder Bot');
        self.setWindowIcon(QtGui.QIcon('tinder_icon.png'));

        self.show();


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

    tinder = Tinder(fileName="credentials.json");

    recommendations = tinder.getRecommendations();

    for person in recommendations:
        print person.name;

    print("FINISHED");
    app = QtGui.QApplication(sys.argv);
    tinderGui = TinderGui();
    sys.exit(app.exec_());


if __name__ == '__main__':
    main();
   
