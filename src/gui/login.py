import sys
import serial
import time
import struct
import mysql.connector as con
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import *
from Connect import Connect
from Receiver import Receiver

login_ui = uic.loadUiType("login.ui")[0]
register_ui = uic.loadUiType("register.ui")[0]

class RegisterWindow(QDialog, register_ui):
    def __init__(self, DBconn) :
        super().__init__()
        self.setupUi(self)

        # Placeholder text 설정
        self.enterName.setPlaceholderText("Enter the Name")
        self.enterId.setPlaceholderText("Enter the ID")
        self.enterPw.setPlaceholderText("Enter the Password")
        self.enterGoal.setPlaceholderText("Enter the Goal workload")
        self.btnRegister.clicked.connect(self.Register)

        # DB 인스턴스 파라미터 
        self.DBconn = DBconn

    def Register(self):
        name = self.enterName.text()
        id =  self.enterId.text()
        pw = self.enterPw.text()
        goal = self.enterGoal.text()
        
        addlist = [] # 각 요소가 길이 6 크기의 튜플(tup)
        fisrt_query = f"select * from employees where ID = \'{id}\'"
        addlist = self.DBconn.orderQuery(fisrt_query, addlist)
        #print("----------------------------------")
        #print(addlist)
        if (len(addlist) != 0):
            for tup in addlist:
                if id in tup:
                    QMessageBox.warning(self, "Register Output", "Already existing worker info\n Try again with new info!")
                    break
        else:
            second_query = f"insert into employees (NAME, ID, PW, GOAL, CURRENT, AT_WORK) VALUES (\'{name}\',\'{id}\', \'{pw}\', {goal}, 0, 'N')"
            self.DBconn.orderQuery(second_query, is_ = "insert")
            QMessageBox.information(self, "Register Output", "Your info is successfully registered!\n You can login now!")
            # 원래는 Login.ui로 자동 이동

class LoginWindow(QDialog, login_ui):
    loginSuccess = pyqtSignal(str)  # 로그인 성공 시그널, 사용자 ID 전달

    def __init__(self, logrecvFlag, DBconn):
        super().__init__()
        self.setupUi(self)
        self.uid = None 
        
        # Tad data 읽어오기 전까지
        # self.btnLogin.hide()
        # self.btnRegisternow.hide()

        # Placeholder text 설정
        self.editId.setPlaceholderText("ex.83 2B 07 F0")
        self.editPw.setPlaceholderText("ex. nnnn")
        
        # editPw 텍스트 변경 시 'READY TO' show 처리
        self.label_4.hide()
        self.editPw.textChanged.connect(self.PwChanged)
        self.btnLogin.clicked.connect(self.Login)

        # DB 인스턴스 파라미터 
        self.DBconn = DBconn
        
        # 아두이노와 통신 프로토콜 담당 파라미터
        self.BTconn = serial.Serial(port='/dev/ttyACM0', baudrate = 9600, timeout = 1)

        if logrecvFlag == True:
            self.recv = Receiver(self.BTconn)
            self.recv.start()
            print("11111111*login*111111111")
        else:
            print("00000000*login*000000000")
        self.logrecvFlag = logrecvFlag
    
        self.recv.tagged.connect(self.tagged)

    def tagged(self, data):
        print("tagged")
        if data :
            addlist = []
            self.uid = data.decode()
            print("(((((((((((((((((((())))))))))))))))))))")
            QMessageBox.information(self, "Tagged Ouput", "Your ID is available now!\n Please input the password!")
            # Tad data 읽어오면 보이게 하기
            # self.btnLogin.show()
            # self.btnRegisternow.show()
            self.editId.setText(self.uid)
            print(self.uid)
            # print(type(self.uid))            
            query = f"SELECT * FROM employees WHERE ID = \'{self.uid}\'"
            addlist = self.DBconn.orderQuery(query,addlist)
            print(addlist)
            print("(((((((((((((((((((())))))))))))))))))))")
        else :
            print(0)
        return
    
    def PwChanged(self, text):
        # 입력된 텍스트가 비어 있지 않으면 label_4 보이기
        if text:
            self.label_4.show()

    def Login(self):
        id = self.editId.text()
        pw = self.editPw.text()
        addlist = []
        query = f"select * from employees where ID = \'{id}\' and PW = \'{pw}\'"
        addlist = self.DBconn.orderQuery(query, addlist)
        # print("---------------------------------")
        # print(addlist)
        if (len(addlist) != 0):
            for tup in addlist:
                if (id in tup) and (pw in tup):
                    QMessageBox.information(self, f"Login Output", "Welcome to 산지직송(주)!\n You login successfully!")
                    self.editId.clear()
                    self.editPw.clear()
                    break
            # 안전 장치
            if self.logrecvFlag == True:
                self.recv.stop()
                
                # 로그인 성공 시그널 발생
                self.loginSuccess.emit(id) 

        else:
            QMessageBox.warning(self, "Login Output", "Invalid User info!\n Try again or Register new info!")
            self.editId.clear()
            self.editPw.clear()

if __name__ == "__main__" :
    # 프로그램 실행
    app = QApplication(sys.argv)
    DBconn = Connect("manager", "0000") 
    # 화면 전환용 Widget 설정
    widget = QtWidgets.QStackedWidget()
    # 레이아웃 인스턴스 생성
    loginwindow = LoginWindow(True, DBconn)
    registerwindow = RegisterWindow(DBconn)   
    # Widget 추가
    widget.addWidget(loginwindow)
    widget.addWidget(registerwindow)
    # 프로그램 화면 보이기
    # 처음 화면
    widget.setCurrentIndex(0)
    widget.setFixedHeight(600)
    widget.setFixedWidth(600)
    widget.show() 

    #프로그램 종료까지 동작시킴
    app.exec_()
    # 애플리케이션 종료 시 DB 연결 종료
    DBconn.disConnection()
