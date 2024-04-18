import sys 
import serial
import struct
import mysql.connector
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5 import uic 
from PyQt5.QtCore import *

class Receiver(QThread):
    detected = pyqtSignal(bytes) #OF
    c_sensored = pyqtSignal(bytes) #CS
    tagged =  pyqtSignal(bytes) #ID

    def __init__(self, conn, parent = None):
        super(Receiver, self).__init__(parent)
        self.is_running = False
        self.conn = conn 
        print("recv init")
    
    def run(self):
        print("recv start")
        self.is_running = True
        while(self.is_running == True):
            if self.conn.readable():
                respond = self.conn.read_until(b'\n')
                if len(respond) > 0 :
                    respond = respond[:-2]
                    cmd = respond[:2].decode()
                    if cmd == 'OF': 
                        print("recv detected")
                        self.detected.emit(respond[2:])
                    elif cmd == 'CS': 
                        print("recv color sensor value")
                        self.detected.emit(respond[2:])
                    elif cmd == 'ID': 
                        print("recv UID")
                        self.detected.emit(respond[2:])
                    else : 
                        print("unknown error")
                        print(cmd)
                print("-------------------")
    
    def stop(self):
        print("recv stop")
        self.is_running = False

from_class = uic.loadUiType("home.ui")[0]

class WindowClass(QMainWindow, from_class) :
    def __init__(self) :
        super().__init__()

        self.setupUi(self)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.conn = serial.Serial(port='/dev/ttyACM0', baudrate = 9600, timeout = 1)

        self.recv = Receiver(self.conn)
        self.recv.start()

        self.recv.detected.connect(self.detected)
        self.recv.c_sensored.connect(self.c_sensored)
        self.recv.tagged.connect(self.tagged)

    def detected(self,data):
        print("detected")
        if data :
            print(1)
        else :
            print(0)
        return
    
    def c_sensored(self,data):
        print("c_sensored")
        if data :
            print(1)
        else :
            print(0)
        return
    
    def tagged(self,data):
        print("tagged")
        if data :
            print(1)
        else :
            print(0)
        return


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_()) 
