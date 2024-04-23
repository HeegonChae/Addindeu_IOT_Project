import sys
import serial
import time
import struct
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Receiver(QThread):
    # '센서에 감지됨'을 전달하는 시그널
    detected = pyqtSignal(bytes) #OF
    c_sensored = pyqtSignal(bytes) #CS
    tagged =  pyqtSignal(bytes) #ID

    def __init__(self, conn, parent = None):
        super(Receiver, self).__init__(parent)
        self.is_running = False
        self.conn = conn
        print("home recv init")

    def run(self):
        print("home recv start")
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
                        print(respond[2:].decode())
                        print("------------------------")
                        self.detected.emit(respond[2:])
                    elif cmd == 'CS':
                        print("recv color sensor value")
                        print(respond[2:].decode())
                        print("------------------------")
                        self.c_sensored.emit(respond[2:])
                    elif cmd == 'ID':
                        print("recv UID")
                        print(respond[2:].decode())
                        print("------------------------")
                        self.tagged.emit(respond[2:])
                    else :
                        print("recv unknown cmd")
                        print(recv_test)
                print("running home recv...")
                time.sleep(3)

    def stop(self):
        print("home recv stop")
        self.is_running = False