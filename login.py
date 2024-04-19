import sys 
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5 import uic 
import mysql.connector as con
from home import * 

login_ui = uic.loadUiType("./src/login.ui")[0]
register_ui = uic.loadUiType("./src/register.ui")[0]
home_ui = uic.loadUiType("./src/home.ui")[0]

class RegisterWindow(QDialog, register_ui):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        
        # Placeholder text 설정
        self.enterName.setPlaceholderText("Enter the Name") 
        self.enterId.setPlaceholderText("Enter the ID") 
        self.enterPw.setPlaceholderText("Enter the Password") 
        self.enterGoal.setPlaceholderText("Enter the Goal workload") 

        self.btnRegister.clicked.connect(self.Register)
        self.btnLoginnow.clicked.connect(self.LoginOpen)

    def dbConnection(self):
        conn = con.connect(
            host = "database-1.cdigc6umyoh0.ap-northeast-2.rds.amazonaws.com",
            port = 3306,
            user = "manager",
            password = "0000",
            database ="smartfarmdb"
            )
        cursor = conn.cursor(buffered=True)
        return conn, cursor

    def disConnection(self, conn):
        conn.close()
    
    def orderQuery(self, query, addlist = '', is_select = True):
        # DB 연결 시작
        conn, cursor = self.dbConnection()
        # Query 실행
        cursor.execute(query)

        if is_select:
            if (len(addlist) == 0):
                result = cursor.fetchone()
                # DB 연결 종료
                self.disConnection(conn)
                return conn, result
            else:
                result = cursor.fetchall()
                for row in result:
                    addlist.append(row)
                print(addlist)
                # DB 연결 종료
                self.disConnection(conn)
                #return conn, addlist
        else:
            conn.commit()  # INSERT, UPDATE, DELETE 등은 commit 필요
            self.disConnection(conn)
            return None, None
        
    def Register(self):
        name = self.enterName.text()
        id =  self.enterId.text()
        pw = self.enterPw.text()
        goal = self.enterGoal.text()
        # print(name)
        _, result = self.orderQuery(f"select * from employees where PW = \'{pw}\'")
        # print("----------------------------")
        # print(result)
        if (result is not None and pw in result):
            QMessageBox.warning(self, "Register Output", "Already existing worker info\n Try again with new info!")
        else:
            _, _ = self.orderQuery(f"insert into employees (NAME, ID, PW, GOAL, CURRENT, AT_WORK) VALUES (\'{name}\',\'{id}\', \'{pw}\', {goal}, {0}, \'{0}\')",
                                   is_select = False)
            QMessageBox.information(self, "Register Output", "Your info is successfully registered!\n You can login now!")
            self.LoginOpen()

    def LoginOpen(self):
        self.enterName.clear()
        self.enterId.clear()
        self.enterPw.clear()
        self.enterGoal.clear()
        widget.setCurrentIndex(0)

class LoginWindow(QDialog, login_ui) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        # Placeholder text 설정
        self.editId.setPlaceholderText("ex.Chae") 
        self.editPw.setPlaceholderText("ex. 83 2B 07 F0") 

        # editPw 텍스트 변경 시 'READY TO' show 처리
        self.label_4.hide()
        self.editPw.textChanged.connect(self.PwChanged)

        self.btnLogin.clicked.connect(self.Login)
        self.btnRegisternow.clicked.connect(self.RegisterOpen)

    def dbConnection(self):
        conn = con.connect(
            host = "database-1.cdigc6umyoh0.ap-northeast-2.rds.amazonaws.com",
            port = 3306,
            user = "chae",
            password = "0111",
            database ="smartfarmdb"
            )
        cursor = conn.cursor(buffered=True)
        return conn, cursor

    def disConnection(self, conn):
        conn.close()
    
    def orderQuery(self, query, addlist = ''):
        # DB 연결 시작
        conn, cursor = self.dbConnection()
        # Query 실행
        cursor.execute(query)

        if (len(addlist) == 0):
            result = cursor.fetchone()
            # DB 연결 종료
            self.disConnection(conn)
            return conn, result
        else:
            result = cursor.fetchall()
            for row in result:
                addlist.append(row)
            print(addlist)
            # DB 연결 종료
            self.disConnection(conn)
            #return conn, addlist

    def PwChanged(self, text):
        # 입력된 텍스트가 비어 있지 않으면 label_4 보이기
        if text:
            self.label_4.show()

    def RegisterOpen(self):
        self.editId.clear()
        self.editPw.clear()
        widget.setCurrentIndex(1)


    def Login(self):
        id = self.editId.text()
        pw = self.editPw.text()
        
        _, result = self.orderQuery(f"select * from employees where ID = \'{id}\' and PW = \'{pw}\'")
        # print("----------------------------")
        # print(result)
        if result:
            QMessageBox.information(self, "Login Output", "Welcome to 산지직송(주)!\n You login successfully!")
            widget.setCurrentIndex(2)
        else:
            QMessageBox.warning(self, "Login Output", "Invalid User info!\n Try again or Register new info!")


# ChangeWindow 함수 수정
def ChangeWindow(index):
    if index == 2:  # HomeWindow의 인덱스가 2일 때
        widget.setFixedSize(1064, 595)  # HomeWindow에 맞는 크기 설정
    else:
        widget.setFixedSize(600, 600)  # 다른 윈도우에 맞는 기본 크기 설정

if __name__ == "__main__" :
    # 프로그램 실행
    app = QApplication(sys.argv)
    # 화면 전환용 Widget 설정
    widget = QtWidgets.QStackedWidget()
    # 레이아웃 인스턴스 생성
    loginwindow = LoginWindow()
    registerwindow = RegisterWindow()   
    homewindow = HomeWindow()
    # Widget 추가
    widget.addWidget(loginwindow)
    widget.addWidget(registerwindow)
    widget.addWidget(homewindow)
    # 프로그램 화면 보이기
    # 처음 화면
    widget.setCurrentIndex(0)
    widget.setFixedHeight(600)
    widget.setFixedWidth(600)
    widget.show() 
    # 레이아웃 인스턴스 전환에 따른 창 크기 변경
    widget.currentChanged.connect(ChangeWindow)
    #프로그램 종료까지 동작시킴
    sys.exit(app.exec_()) 