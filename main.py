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
        
        # 화면 전환용 Widget 설정
        self.widget = QStackedWidget()
       
        # 레이아웃 인스턴스 생성
        self.loginwindow = LoginWindow(True, DBconn)
        self.registerwindow = RegisterWindow(DBconn)
        
        # 화면 전환 시그널 연결
        self.loginwindow.btnRegisternow.clicked.connect(self.showRegister)
        self.registerwindow.btnLoginnow.clicked.connect(self.showLogin)
        
        # Widget에 각 창 추가
        self.widget.addWidget(self.loginwindow)
        self.widget.addWidget(self.registerwindow)
        
        # 초기 화면 설정
        self.widget.setCurrentIndex(0)
        
        # Widget을 메인 UI로 설정
        self.setLayout(self.widget.layout())
        
        # 창 크기 고정
        self.setFixedSize(600, 600)
    
    def showLogin(self):
        self.registerwindow.enterName.clear()
        self.registerwindow.enterId.clear()
        self.registerwindow.enterPw.clear()
        self.registerwindow.enterGoal.clear()
        self.widget.setCurrentIndex(0)
    
    def showRegister(self):
        self.loginwindow.editId.clear()
        self.loginwindow.editPw.clear()
        self.widget.setCurrentIndex(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # DB 연결 생성
    DBconn = Connect("manager", "0000") 
    
    main_ui = MainUI(DBconn)
    main_ui.show()
    logrecvFlag = main_ui.loginwindow.logrecvFlag
    print(f'Login.py에서 넘어온 recvFlag : {logrecvFlag}') 
    
    app.exec_()
    # 애플리케이션 종료 시 DB 연결 종료
    DBconn.disConnection()