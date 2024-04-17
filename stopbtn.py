import sys
import serial
import time
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

# 시리얼 포트 설정
serial_port = '/dev/ttyACM0'
baud_rate = 9600
bt_serial = serial.Serial(serial_port, baud_rate, timeout=1)

from_class = uic.loadUiType("stopbtn.ui")[0]

class WindowClass(QMainWindow, from_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.btnEStop.clicked.connect(self.btnPressed)
    
    def btnPressed(self):
        #self.editState.clear()
        self.textBrowser.append("Button Pressed " + self.currentTime())
        try:
                bt_serial.write(b'Button Pressed\n')
                self.textBrowser.append("Data sent to Arduino" + self.currentTime())
        except Exception as e:  
                self.textBrowser.append("Error:", e)
    
    def currentTime(self):
        return QDateTime.currentDateTime().toString("yy-MM-dd hh:mm:ss")

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()

    sys.exit(app.exec_())