import sys
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from login import LoginWindow, RegisterWindow
from home import HomeWindow
from Connect import Connect

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
        self.homewindow = HomeWindow(True, DBconn)
        # home.ui tableWidget 초기화 
        self.tableWidget = self.homewindow.tableWidget
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Widget에 창 추가
        self.widget.addWidget(self.homewindow)
        # home.ui 창 열기 
        self.widget.setCurrentIndex(2)
        # home.ui와 DB 연동
        self.ShowWorkerInfo()

    def ShowWorkerInfo(self):
        # print(f"User logged in with ID: {self.worker_uid}")
        addlist = []
        query = f"select Name, ID, PW, GOAL from employees where ID = \'{self.worker_uid}\'"
        addlist = self.DBconn.orderQuery(query, addlist)
        workerInfo = addlist[0]
        name = workerInfo[0]; id = workerInfo[1]; pw = workerInfo[2]; goal = workerInfo[3]

        # 로그인에서 입력 받은 데이터 home.ui TableWidget에 보이기
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, QTableWidgetItem(name))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(id))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(pw))
        self.tableWidget.setItem(row, 3, QTableWidgetItem(str(goal)))

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

