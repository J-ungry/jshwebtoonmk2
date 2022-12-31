import pymysql


#DB_USER="jsh"   #MySQL 계정명
DB_USER = "root" #정구리 MySQL 계정명
DB_NAME="jsh"   #MySQL DB명

# cursor 생성 함수
def create_cursor(db):
    cursor=db.cursor()
    return cursor

def conn():
    webtoon_db = pymysql.connect(   
        host="localhost",
        port=3306,
        user=DB_USER,
        #passwd="bread!123",
        passwd="duffufK123!",
        db=DB_NAME,
        charset="utf8"
        )
    print("connect MySQL🎉")
    return webtoon_db

def select_query(db, query):
    cursor=create_cursor(db)
    cursor.execute(query)
    datas = cursor.fetchall()
    return datas

def update_query(db, query):
    cursor=create_cursor(db)
    cursor.execute(query)
    result = db.commit()
    return result  

