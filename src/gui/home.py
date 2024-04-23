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


home_ui = uic.loadUiType("home.ui")[0]
class HomeWindow(QDialog, home_ui) :
    logoutSuccess = pyqtSignal(str)  # 로그아웃 성공 시그널

    def __init__(self, homerecvflag, DBconn) :
        super().__init__()
        self.setupUi(self)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
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

        # count변수
        self.p = 0
        self.np = 0
        self.total = self.p + self.np

        # DB 인스턴스 파라미터 
        self.DBconn = DBconn
        # ON/OFF 클릭 I/O 상태
        self.powerBtnState = False
        # 로그인 성공 후 전달 받을 ID??
        self.uid = None
        # 아두이노와 통신 프로토콜 담당
        self.BTconn = serial.Serial(port='/dev/ttyACM0', baudrate = 9600, timeout = 1)

        if homerecvflag == True:
            self.recv = Receiver(self.BTconn)
            self.recv.start()
            print("111111111*home*11111111")
            # 타이머 시작
            self.timer.start()
            homerecvflag = False
        else:
            print("000000000*home*000000000")
        self.homerecvflag = homerecvflag

        self.recv.detected.connect(self.detected)
        self.recv.c_sensored.connect(self.c_sensored)
        self.recv.tagged.connect(self.tagged)
        
        # Emergency Stop 버튼 이벤트 처리
        self.btnEmergency.clicked.connect(self.EmergencyStop)
        # Power 버튼 이벤트 처리
        self.btnPower.clicked.connect(self.PowerState)
        self.btnPower.setStyleSheet("background-color: green;")
        self.btnEmergency.setStyleSheet("background-color: red;")

        self.updateText(self.editNow,'-')
        self.updateText(self.editGoal,'-')
        self.updateText(self.editP,'-')
        self.updateText(self.editNp,'-')
    
    def LogOut(self):
        # 안전장치
        if self.homerecvflag == False: 
            self.logoutSuccess.emit("logout")
            # # 아두이노에서 받기 종료
            # self.recv.stop()
            # # 타이머 종료
            # self.timer.stop()
    
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
        
    def detected(self,data):
        print("detected")
        if data :
            print(data.decode())
            #print(type(data.decode()))
            if data.decode() == '1' :
                QMessageBox.information(self,'인식 성공','인식에 성공했습니다. 작업을 시작하세요.')
            else : 
                QMessageBox.warning(self,'인식 실패','인식 실패. 인식을 재시도합니다.')
        else :
            QMessageBox.warning(self,'통신 오류','통신에 실패하였습니다.')
            
        return
    
    def c_sensored(self,data):
        print("c_sensored")
        if self.total >= self.goal :
            QMessageBox.information(self,'작업 완료','열심히 일한자, 퇴근하라.')
            self.recv.stop()
            self.TaskFinish()
        else :
            if data :
                print(data.decode())
                #print(type(data.decode()))
                if data.decode() == '1' :
                    query = f"UPDATE employees SET pass = pass + 1 WHERE ID = \'{self.uid}\'"
                    print(query)
                    self.p += 1
                    self.updateText(self.editP,self.p)
                else : 
                    query = f"UPDATE employees SET NonPass = NonPass + 1 WHERE ID = \'{self.uid}\'"
                    print(query)
                    self.np += 1
                    self.updateText(self.editNp,self.np)
                    self.DBconn.executeQuery(query)
                query = f"UPDATE employees SET CURRENT = NonPass + Pass WHERE ID = \'{self.uid}\'"
                print(query)
                self.DBconn.executeQuery(query)
                self.total = self.p + self.np
                self.updateText(self.editNow,self.total)
            else :
                QMessageBox.warning(self,'통신 오류','통신에 실패하였습니다.')
        return
    
    def tagged(self,data):
        print("tagged")
        if data :
            addlist = []
            self.p = 0
            self.np = 0
            self.updateText(self.editP,self.p)
            self.updateText(self.editNp,self.np)
            self.uid = data.decode()
            print(self.uid)
            query = f"SELECT * FROM employees WHERE ID = \'{self.uid}\'"
            print(query)
            addlist = self.DBconn.orderQuery(query,addlist)
            print(addlist)
            query = f"UPDATE employees SET NonPass = 0 WHERE ID = \'{self.uid}\'"
            print(query)
            self.DBconn.executeQuery(query)
            query = f"UPDATE employees SET Pass = 0 WHERE ID = \'{self.uid}\'"
            print(query)
            self.DBconn.executeQuery(query)
            query = f"UPDATE employees SET CURRENT = 0 WHERE ID = \'{self.uid}\'"
            print(query)
            self.DBconn.executeQuery(query)
            query = f"SELECT * FROM employees WHERE ID = \'{self.uid}\'"
            print(query)
            addlist = []
            addlist = self.DBconn.orderQuery(query,addlist)
            self.goal = addlist[0][3]
            self.updateText(self.editGoal,self.goal)
        else :
            QMessageBox.warning(self,'통신 오류','통신에 실패하였습니다.')
        return
    
    def Send(self,command, flag=0):
        print("send flag")
        data = struct.pack('<2sic', command, flag, b'\n')
        self.BTconn.write(data)
        print(data)
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
        print("Finished")
        self.Send(b'FN')
        time.sleep(0.1)
    
    def updateText(self,name,value):
        value = str(value)
        name.setText(value)
        name.setAlignment(Qt.AlignCenter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    DBconn = Connect("manager", "0000") 

    # Connect 클래스의 인스턴스가 생성되었는지 확인 후 HomeWindow 객체 생성
    if DBconn.conn is not None:
        myWindow = HomeWindow(True, DBconn)
        myWindow.show()
        app.exec_()
        # 애플리케이션 종료 시 DB 연결 종료
        DBconn.disConnection()
    else:
        print("DB 연결 실패!")
        app.exec_()