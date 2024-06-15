import mysql.connector as con

class Connect():
    def __init__(self,User,Password):
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

    def orderQuery(self, query, addlist=[], is_='select'):
        # Query 실행
        self.cursor.execute(query)

        if is_ == 'select':
            result = self.cursor.fetchall()
            for row in result:
                addlist.append(row)
            return addlist
        else:
            self.conn.commit()
            print("DONE")

    def executeQuery(self, query):
        print("query ok")
        self.cursor.execute(query)
        print("execute ok")
        self.conn.commit()
        print("commit ok")

        
if __name__ == "__main__" :
    db_instance = Connect("manager", "0000")
    addlist = []

    # Case 1.
    query = "UPDATE employees SET pass = pass + 1 WHERE ID = \'0A 0B 0C 0D\'"
    db_instance.executeQuery(query)
    # Case 2.
    query = "SELECT * FROM employees WHERE ID = \'0A 0B 0C 0D\'"
    addlist = db_instance.orderQuery(query, addlist)
    print(addlist)

    db_instance.disConnection()


