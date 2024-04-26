import sys
import serial
import time
import struct
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import *
from Connect import Connect
from Receiver import *
import requests
import json

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

        self.Setup()

    def Setup(self):
        # 타이머 관련 위젯
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.Showtime)
        self.lcdTimer.display('')
        self.lcdTimer.setDigitCount(8)

        # 날씨 관련 파라미터
        self.forecastApi = "6e357d11903a3df81c1cff95bca0f2af"
        self.location = "Seoul" 
        self.lang = 'kr' #언어
        self.units = 'metric' #화씨 온도를 섭씨 온도로 변경
        self.timer.start()
    
    def Showtime(self):
        # 날짜
        datetime = QDateTime.currentDateTime()
        self.labelDate.setText(datetime.toString('yyyy-MM-dd'))
        # 시간
        sender = self.sender()
        currentTime = QTime.currentTime().toString("hh:mm:ss")
        if id(sender) == id(self.timer):
            self.lcdTimer.display(currentTime)
        # 날씨
        self.ShowForecast()

    def ShowForecast(self):
        api = f"https://api.openweathermap.org/data/2.5/weather?q={self.location}&appid={self.forecastApi}&lang={self.lang}&units={self.units}"

        result = requests.get(api)
        result = json.loads(result.text)
        weather = result['weather'][0]['main']
        degree = result['main']['temp']
        self.labelWeather.setText(str(degree) + '\u2103'+'\n'+weather)

    def Search(self):
        self.tableWidget.clearContents()
        userName = self.editName.text()
        #userId =  self.editId.text()

        addlist = []
        query = f"select NAME, ID, GOAL, AT_WORK from employees where NAME = \'{userName}\'"
        addlist = self.DBconn.orderQuery(query, addlist)
        if len(addlist) == 0:
            QMessageBox.warning(self, "Search Output", "Not in our company!\nTry again with new info!")
            self.editName.clear()
            self.editId.clear()
            return
        
        workerInfo = addlist[0]
        name = workerInfo[0]; id = workerInfo[1]; goal = workerInfo[2]; at_work = workerInfo[3]
        
        row = self.tableWidget.rowCount()  
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, QTableWidgetItem(name))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(id))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(str(goal)))
        self.tableWidget.setItem(row, 3, QTableWidgetItem(at_work))

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