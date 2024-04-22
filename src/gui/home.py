import sys
import serial
import time
import struct
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import *
from Connect import Connect
import requests
import json

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
                        self.detected.emit(respond[2:])
                    elif cmd == 'CS':
                        print("recv color sensor value")
                        self.c_sensored.emit(respond[2:])
                    elif cmd == 'ID':
                        print("recv UID")
                        self.tagged.emit(respond[2:])
                    else :
                        print("recv unknown cmd")
                        print(recv_test.decode())
                print("running home recv...")
                time.sleep(3)

    def stop(self):
        print("home recv stop")
        self.is_running = False

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
        # Logout 버튼 이벤트 처리
        self.btnLogOut.clicked.connect(self.LogOut)

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
            #self.uid = data
        else :
            print(0)
        return
    
    def Send(self,command, flag=0):
        print("send flag")
        data = struct.pack('<2sic', command, flag, b'\n')
        self.BTconn.write(data)
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
    DBconn = Connect("manager", "0000") 
    myWindows = HomeWindow(True, DBconn)
    myWindows.show()
    DBconn.disConnection()
    sys.exit(app.exec_())