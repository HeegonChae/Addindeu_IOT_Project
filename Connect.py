import mysql.connector as con

class Connect():
    def __init__(self,User,Password):
         # DB 연결 시작
        self.conn = con.connect(
            host = "database-1.cdigc6umyoh0.ap-northeast-2.rds.amazonaws.com",
            port = 3306,
            user = User,
            password = Password,
            database ="smartfarmdb"
            )
        self.cursor = self.conn.cursor(buffered=True)

    def disConnection(self):
        self.conn.close()

    def orderQuery(self, query, addlist, is_ = 'select'):
        # Query 실행
        self.cursor.execute(query)

        if is_ == 'select':
            result = self.cursor.fetchall()
            for row in result:
                addlist.append(row)
            #print("------------------------")
            #print(addlist)
            # DB 연결 종료
            self.disConnection()
        else:
            self.conn.commit()  # INSERT, UPDATE, DELETE 등은 commit 필요
            self.disConnection()
  
        
if __name__ == "__main__" :
    db_instance = Connect("manager", "0000")
    addlist = []
    query = "select * from employees"
    
    db_instance.orderQuery(query, addlist)