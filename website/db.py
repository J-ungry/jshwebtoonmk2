import pymysql

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
    