import sys 
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5 import uic 

from_class = uic.loadUiType("login.ui")[0]

class WindowClass(QMainWindow, from_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

if __name__ == "__main__" :
    app = QApplication(sys.argv) #프로그램 실행
    myWindows = WindowClass() #화면 클래스 생성
    myWindows.show() #프로그램 화면 보이기
    sys.exit(app.exec_()) #프로그램 종료까지 동작시킴
