import sys 
import serial
import struct
import mysql.connector
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5 import uic 
from PyQt5.QtCore import *
'''
class Receiver(QThread):
    detected = pyqtSignal(bytes)

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
                    respond = respond[:-2] #구분자 삭제 '\r\n'
                    cmd = respond[:2].decode()
                    if cmd == 'GS' and respond[2] == 0 : 
                        print("recv detected")
                        self.detected.emit(respond[3:])
                    else : 
                        print("unknown error")
                        print(cmd)
    
    def stop(self):
        print("recv stop")
        self.is_running = False

'''
from_class = uic.loadUiType("home.ui")[0]

class WindowClass(QMainWindow, from_class) :
    def __init__(self) :
        super().__init__()

        self.setupUi(self)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def dbConnection(self):
        self.conn = mysql.connector.connect(
        host = "localhost",
        port = 3306,
        user = "root",
        password = "****",
        database ="iot_project"
        )
        self.cursor = self.conn.cursor(buffered=True)
    
    def disConnection(self):
        self.conn.close()
    
    def orderQuery(self,query,addlist):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        for row in result:
            addlist.append(row)
        print(addlist)
        self.conn.close()


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_()) 
