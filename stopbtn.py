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

from_class = uic.loadUiType("stopbtn.ui")[0]

class WindowClass(QMainWindow, from_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.bt_serial = serial.Serial(serial_port, baud_rate, timeout=1)

        self.btnEStop.clicked.connect(self.btnPressed)
    
    def btnPressed(self):
        #self.editState.clear()
        self.textBrowser.append("Button Pressed " + self.currentTime())
        try:
             self.sendData()
             self.recvData()
        except Exception as e:  
                self.textBrowser.append("Error:", e)
    
    def sendData(self):
         self.bt_serial.write('Button Pressed\n'.encode())
         self.textBrowser.append("Data sent to Arduino" + self.currentTime())
         time.sleep(0.1)
    
    def recvData(self):
          if(self.bt_serial.readable()):
            recv = self.bt_serial.readline().decode().strip('\r\n')
            if(len(recv) > 0):
                self.textBrowser.append("recv : " + str(recv))
         
    
    def currentTime(self):
        return QDateTime.currentDateTime().toString("yy-MM-dd hh:mm:ss")

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()

    sys.exit(app.exec_())