import sys 
import serial
import time
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
                recv_test = respond
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
                        print("recv unknown cmd")
                        print(recv_test.decode())
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

        self.powerBtnState = False

        self.recv.detected.connect(self.detected)
        self.recv.c_sensored.connect(self.c_sensored)
        self.recv.tagged.connect(self.tagged)

        self.btnEmergency.clicked.connect(self.EmergencyStop)
        self.btnPower.clicked.connect(self.PowerState)
        self.btnPower.setStyleSheet("background-color: green;")

    def detected(self,data):
        print("detected")
        if data :
            print(1)
            QMessageBox.information(self,'인식 성공','인식에 성공했습니다. 작업을 시작하세요.')
            
        else :
            print(0)
            QMessageBox.warning(self,'인식 실패','인식 실패. 인식을 재시도합니다.')
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
    
    def Send(self,command, flag=0):
        print("send flag")
        data = struct.pack('<2sic', command, flag, b'\n')
        self.conn.write(data)
        return
    
    def PowerState(self):
        if self.powerBtnState == False:
            self.btnPower.setStyleSheet("background-color: red;")
            self.btnPower.setText("OFF")
            self.PowerOn()
            self.powerBtnState = True
        else :
            self.btnPower.setStyleSheet("background-color: green;")
            self.btnPower.setText("On")
            self.PowerOff()
            self.powerBtnState = False

    
    def EmergencyStop(self):
        print("Emergency Stop")
        self.Send(b'EM')
        time.sleep(0.1)

    def PowerOn(self):
        print("Power On")
        self.Send(b'PF',1)
        time.sleep(0.1)
    
    def PowerOff(self):
        print("Power Off")
        self.Send(b'PF')
        time.sleep(0.1)

    def TaskFinish(self):
        print("Emergency Stop")
        self.Send(b'FN')
        time.sleep(0.1)


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_()) 
