import sys
from PyQt4 import QtGui

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
   
