import mysql.connector as con
class Connect():
    def __init__(self,user,password):
            self.conn = con.connect(
                host = "database-1.cdigc6umyoh0.ap-northeast-2.rds.amazonaws.com",
                port = 3306,
                user = user,
                password = password,
                database ="smartfarmdb"
                )
            self.cursor = self.conn.cursor(buffered=True)

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
