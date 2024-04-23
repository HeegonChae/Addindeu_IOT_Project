import sys
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from login import LoginWindow, RegisterWindow
from home import HomeWindow
from Connect import Connect

import serial
import time
import struct
import requests
import json

class MainUI(QWidget): 
    
    def __init__(self, DBconn):
        super().__init__()
        self.worker_uid = None

        # 화면 전환용 Widget 설정
        self.widget = QStackedWidget()

        # 레이아웃 인스턴스 전환에 따른 창 변경
        self.widget.currentChanged.connect(self.ChangeWindowsize)

        # 레이아웃 인스턴스 생성
        self.loginwindow = LoginWindow(True, DBconn)
        self.registerwindow = RegisterWindow(DBconn)
        self.homewindow = None
        self.tableWidget = None

        self.DBconn = DBconn
        
        # 화면 전환 시그널 연결
        self.loginwindow.btnRegisternow.clicked.connect(self.ShowRegister)
        self.registerwindow.btnLoginnow.clicked.connect(self.ShowLogin)
        
        # 로그인 성공 시그널 확인 
        self.loginwindow.loginSuccess.connect(self.OnLoginSuccess)

        # Widget에 각 창 추가
        self.widget.addWidget(self.loginwindow)
        self.widget.addWidget(self.registerwindow)

        # 초기 화면 설정
        self.widget.setCurrentIndex(0)
        self.resize(600, 600)  

        # Widget을 메인 UI로 설정
        self.setLayout(self.widget.layout())

    def OnLoginSuccess(self, userid):
        self.worker_uid = userid
        # homewinodw 인스턴스 생성
        self.homewindow = HomeWindow(True, userid, DBconn)
        # home.ui tableWidget 초기화 
        self.tableWidget = self.homewindow.tableWidget
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Widget에 창 추가
        self.widget.addWidget(self.homewindow)
        # home.ui 창 열기 
        self.widget.setCurrentIndex(2)
        # home.ui와 DB 연동
        self.ShowWorkerInfo()

        # 로그아웃 성공 시그널 확인 
        self.homewindow.logoutSuccess.connect(self.OnLogoutSuccess)
        
    def OnLogoutSuccess(self, msg):
        if msg == "logout":
            # 로그아웃 비교 대상
            goal = self.tableWidget.item(0, 2)
            current = self.tableWidget.item(0, 3)
            if goal is not None:
                goal = goal.text()
                current = current.text()
                # 로그아웃 조건
                if current >= goal:
                    QMessageBox.information(self, "LogOut Output", "Well done! \n You can leave now!")
                     # 아두이노에서 받기 종료
                    self.homewindow.recv.stop()
                    # 타이머 종료
                    self.homewindow.timer.stop()
                    # 초기 로그인 화면으로 리셋
                    self.ResetToLogin()
                else:
                    #QMessageBox.warning(self, "LogOut Output", "Are you sure to leave? \n You have not done yet!")
                    retval = QMessageBox.question(self, "LogOut - Output",
                                "Are you sure to leave? \n You have not done yet!",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    
                    if retval == QMessageBox.Yes:
                       # 일 완료x. 그렇지만 로그아웃
                        # 아두이노에서 받기 종료
                        self.homewindow.recv.stop()
                        # 타이머 종료
                        self.homewindow.timer.stop()
                        self.ResetToLogin()
                    else:
                        return
    
    def ResetToLogin(self):
        # 모든 UI 상태 및 데이터 초기화
        self.widget.removeWidget(self.loginwindow)
        self.widget.removeWidget(self.registerwindow)
        self.widget.removeWidget(self.homewindow)
        # 인스턴스들을 None으로 설정하여 메모리에서 제거
        self.loginwindow = None
        self.registerwindow = None
        self.homewindow = None
        self.tableWidget = None
        # 새로운 인스턴스 생성
        self.loginwindow = LoginWindow(True, self.DBconn)
        self.registerwindow = RegisterWindow(self.DBconn)
        # 새로운 위젯들을 스택에 추가
        self.widget.addWidget(self.loginwindow)
        self.widget.addWidget(self.registerwindow)
        # 초기 로그인 화면으로 설정
        self.widget.setCurrentIndex(0)
        # 필요한 연결 재설정
        self.loginwindow.btnRegisternow.clicked.connect(self.ShowRegister)
        self.registerwindow.btnLoginnow.clicked.connect(self.ShowLogin)
        self.loginwindow.loginSuccess.connect(self.OnLoginSuccess)

        # 리더기에서 다시 TAG DATA 읽어오기
        self.loginwindow.recv.tagged.connect(self.tagged)

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
    
    def updateText(self,name,value):
        value = str(value)
        name.setText(value)
        name.setAlignment(Qt.AlignCenter)
    
    def ShowWorkerInfo(self):
        # print(f"User logged in with ID: {self.worker_uid}")
        addlist = []
        query = f"select Name, ID, GOAL, CURRENT from employees where ID = \'{self.worker_uid}\'"
        addlist = self.DBconn.orderQuery(query, addlist)
        workerInfo = addlist[0]
        name = workerInfo[0]; id = workerInfo[1]; goal = workerInfo[2]; current = workerInfo[3]

        # 로그인에서 입력 받은 데이터 home.ui TableWidget에 보이기
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, QTableWidgetItem(name))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(id))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(str(goal)))
        self.tableWidget.setItem(row, 3, QTableWidgetItem(str(current)))

    def ShowLogin(self):
        self.registerwindow.enterName.clear()
        self.registerwindow.enterId.clear()
        self.registerwindow.enterPw.clear()
        self.registerwindow.enterGoal.clear()
        self.widget.setCurrentIndex(0)

    def ShowRegister(self):
        self.loginwindow.editId.clear()
        self.loginwindow.editPw.clear()
        self.widget.setCurrentIndex(1)      

    def ChangeWindowsize(self, index):
        # 화면 인덱스에 따라 창 크기 조정
        if index == 0 or index == 1:  # Login or Register
            self.resize(600, 600)
        elif index == 2:              # Home
            self.resize(1064, 595)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # DB 연결 생성
    DBconn = Connect("manager", "0000") 
    # 다른 창과 위젯을 통합하여 전체적인 어플리케이션의 메인 윈도우 역할
    main_ui = MainUI(DBconn)
    main_ui.show()
    app.exec_()
    # 애플리케이션 종료 시 DB 연결 종료
    DBconn.disConnection()

