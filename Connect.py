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
        if self.conn:
            print('!!!!!!DB SHUT DOWN!!!!!!')
            self.conn.close()
            self.conn = None

    def orderQuery(self, query, addlist =[], is_ = 'select'):
        # Query 실행
        self.cursor.execute(query)

        if is_ == 'select':
            result = self.cursor.fetchall()
            for row in result:
                addlist.append(row)
            return addlist
        else:
            self.conn.commit()  # INSERT, UPDATE, DELETE 등은 commit 필요
            print("DONE")
  
        
if __name__ == "__main__" :
    db_instance = Connect("manager", "0000")
    addlist = []

    # Case 1.
    query = "select * from employees"
    addlist = db_instance.orderQuery(query, addlist)
    print(addlist)
    # Case 2.
    query = "insert into employees (NAME, ID, PW, GOAL, CURRENT, AT_WORK) VALUES ('Heegon','2A 2B 2C 2D', '0111', 100, 0, '0')"
    db_instance.orderQuery(query, is_ = 'insert')
    query = "select * from employees"
    addlist = db_instance.orderQuery(query, addlist)
    print(addlist)

    db_instance.disConnection()


