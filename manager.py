import sys 
import serial
import time
import struct
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5 import uic 
from PyQt5.QtCore import *
from Connect import Connect

manager_ui = uic.loadUiType("manager.ui")[0]
class ManagerWindow(QMainWindow, manager_ui) :
    def __init__(self, DBconn) :
        super().__init__()
        self.setupUi(self)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.DBconn = DBconn

        self.btnSerch.clicked.connect(self.Search)
        self.btnEmergency.clicked.connect(self.EmergencyStop)
        #self.BTconn = serial.Serial(port='/dev/rfcomm0', baudrate = 9600, timeout = 1)
        self.BTconn = serial.Serial(port='/dev/ttyACM0', baudrate = 9600, timeout = 1)

    def Search(self):
        userName = self.editName.text()
        userId =  self.editId.text()

        addlist = []
        query = f"select NAME, GOAL, CURRENT, AT_WORK, PASS, NONPASS from employees where NAME = \'{userName}\' and ID = \'{userId}\'"
        addlist = self.DBconn.orderQuery(query, addlist)
        if len(addlist) == 0:
            QMessageBox.warning(self, "Search Output", "Not in our company!\nTry again with new info!")
            self.editName.clear()
            self.editId.clear()
            return
        
        workerInfo = addlist[0]
        name = workerInfo[0]; goal = workerInfo[1]; current = workerInfo[2]; at_work = workerInfo[3]
        p = workerInfo[4]; np = workerInfo[5]
        
        row = self.tableWidget.rowCount()  
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, QTableWidgetItem(name))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(str(goal)))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(str(current)))
        self.tableWidget.setItem(row, 3, QTableWidgetItem(at_work))
        self.tableWidget.setItem(row, 4, QTableWidgetItem(str(p)))
        self.tableWidget.setItem(row, 5, QTableWidgetItem(str(np)))

    def Send(self,command, flag=0):
        print("send flag")
        data = struct.pack('<2sic', command, flag, b'\n')
        self.BTconn.write(data)
        print(data.decode)
        return
    
    def EmergencyStop(self):
        print("Emergency Stop")
        self.Send(b'EM')
        time.sleep(0.1)

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    # DB 연결 생성
    DBconn = Connect("manager", "0000") 
    managerwindow = ManagerWindow(DBconn)
    managerwindow.show()
    app.exec_()
    # 애플리케이션 종료 시 DB 연결 종료
    DBconn.disConnection()