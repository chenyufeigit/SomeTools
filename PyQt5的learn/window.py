from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
class myWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        w.setGeometry(300,300,300,200)
        w.setWindowTitle('window')
        w.setWindowIcon(QIcon(r'C:\Users\yufei.chen\Desktop\Python_scripts\logo.png'))
        w.show()

if __name__=='__main__':
    app=QApplication(sys.argv)
    w=QWidget()
    ex=myWindow()
    sys.exit(app.exec_())

