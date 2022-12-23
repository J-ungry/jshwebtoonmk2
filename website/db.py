import pymysql

#DB_USER="jsh"   #MySQL 계정명
DB_USER = "root" #정구리 MySQL 계정명
DB_NAME="jsh"   #MySQL DB명

# cursor 생성 함수
def create_cursor(db):
    cursor=db.cursor()
    print("create cursor")
    return cursor
        
def query(db,query):
    print(db)
    cursor=create_cursor(db)
    print(cursor)
    print(query)
    cursor.execute(query)
    datas = cursor.fetchall()
    return datas
    