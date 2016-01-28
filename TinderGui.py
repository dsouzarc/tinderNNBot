import sys
from PyQt4 import QtGui

class TinderGui(QtGui.QWidget):

    def __init__(self):
        super(TinderGui, self).__init__();

        self.initUI();

    def initUI(self):
        #x, y, width, height
        self.setGeometry(300, 300, 250, 150);
        self.setWindowTitle('Tinder Bot');
        #self.setWindowIcon(QTGui.QIcon('web.png'));

        self.show();


def main():

    app = QtGui.QApplication(sys.argv);
    tinderGui = TinderGui();
    sys.exit(app.exec_());

if __name__ == '__main__':
    main();
   
