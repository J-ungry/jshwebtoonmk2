from unicodedata import category
from flask import Blueprint,render_template,request,flash,redirect,url_for,session
from werkzeug.security import generate_password_hash,check_password_hash
from website import db
import pymysql
import website.models as models
import datetime

DB_USER="jsh"   #MySQL 계정명
# DB_USER = "root" #정구리 MySQL 계정명
DB_NAME="jsh"   #MySQL DB명

#auth.py에서는 주로 로그인에 관련된 코드 작성
auth = Blueprint("auth",__name__)

webtoon_db = pymysql.connect(   
        host="localhost",
        port=3306,
        user=DB_USER,
        passwd="bread!123",
        # passwd="duffufK123!",
        db=DB_NAME,
        charset="utf8"
        )
print("connect MySQL")

@auth.route("/user_login",methods=["GET","POST"])
def user_login():
    if request.method=="GET":
        return render_template("login.html")
    elif request.method=="POST":
        id=request.form.get("id")   #name 속성 값이 id인 input 가져옴(사용자가 입력한 값 가져옴)
        password=request.form.get("password")
        #쿼리문 안에 변수 쓸 때 포매팅으로 f 쓰는데 '{변수}' 처럼 따옴표 꼭 붙여야 함
        select_user=db.query(webtoon_db,f"SELECT * FROM user WHERE id='{id}'")
        print(select_user)
        login_user_check=select_user[0]
        print(login_user_check)
        
        login_user_id=login_user_check[0]
        login_user_password=login_user_check[1]
        
        #flash는 js에서 alert랑 똑같은 기능(알람)
        #category는 success랑 error로 분류. 말 그대로 문제 있는 걸 알려주려면 error 문제 없음 success
        if id not in login_user_id:
            flash("아이디가 존재하지 않습니다.",category="error")
        elif password!=login_user_password:
            flash("비밀번호가 틀립니다.",category="error")
        elif len(id)<1:
            flash("아이디를 입력하세요",category="error")
        elif len(id)>=1 and len(id)<5:
            flash("아이디는 5글자 이상입니다.",category="error")
        else:
            user_name=login_user_check[2]
            user_age=login_user_check[3]
            user_gender=login_user_check[4]
            
            #session 등록하기 위해서는 필수. 생략 안됨
            from main import app
            app.secret_key="kth"
            
            #session에서 id는 user_id,name은 user_name,age는 user_age,gender는 user_gender
            session["user_id"]=id
            session["user_name"]=user_name
            session["user_age"]=user_age
            session["user_gender"]=user_gender
            flash("로그인 성공",category="success")
            
            #index.html은 views.py에 등록되어 있어서 views에 보내야함
            return redirect(url_for("views.index"))
        return render_template("login.html")

@auth.route("/sign_up",methods=["GET","POST"])
def sign_up():
    if request.method=="GET":
        return render_template("sign_up.html")
    elif request.method=="POST":
        id=request.form.get("id")
        name=request.form.get("name")
        password=request.form.get("password")
        repassword=request.form.get("repassword")
        gender=request.form.get("gender")
        age=request.form.get("age")
        
        check_id=db.query(webtoon_db,f"SELECT id FROM user WHERE id='{id}'")
        print(check_id)
        
        if check_id:
            flash("이미 존재하는 아이디입니다.",category="error")
        else:
            if len(id)<5:
                flash("아이디는 5자 이상입니다.",category="error")
            elif len(name)<2:
                flash("이름은 3글자 이상입니다.",category="error")
            elif password != repassword:
                flash("비밀번호와 비밀번호재입력이 다릅니다.",category="error")
            elif len(password)<7:
                flash("비밀번호가 너무 짧습니다.",category="error")
            elif gender=="else":
                flash("성별을 선택해주세요.",category="error")
            elif age=="else":
                flash("연령대를 선택해주세요.",category="error")
            else:
                insert_user_data=f"INSERT INTO user VALUES ('{id}','{password}','{name}','{age}','{gender}')"
                check=db.query(webtoon_db,insert_user_data)
                print(check)
                print(type(check))
               
                webtoon_db.commit()
                flash("회원가입 완료.",category="success")
                return redirect(url_for("views.index"))
        
    return render_template("sign_up.html")

@auth.route("/logout",methods=["GET"])
def logout():
    #session에 등록되어 있는 정보 삭제
    session.pop("user_id",None)
    session.pop("user_name",None)
    session.pop("user_age",None)
    session.pop("user_gender",None)
    flash("로그아웃되었습니다.",category="success")
    return render_template("index.html")

@auth.route("/user_detail",methods=["GET"])
def user_detail():
    if request.method=="GET":
        if session:
            dates=db.query(webtoon_db,f"select DISTINCT rcm_date from history where user_id='{session['user_id']}' order by rcm_date desc")
            return render_template("user_detail.html", dates = dates)
        else:
            #flash 안됨
            flash("해당 서비스는 로그인 한 사용자만 이용가능합니다.")
            return redirect(url_for("views.index"))


@auth.route("/recommend/<date>",methods=["GET"])
def recommend(date):
    rcmed_webtoons = db.query(webtoon_db,f"select webtoon_no,rcm_type from history where user_id='{session['user_id']}' and rcm_date='{date}'")

    ds = []
    it = []
    sv = []

    for webtoon in rcmed_webtoons:
        if(webtoon[1] == 'ds'):
            ds.append(db.query(webtoon_db,f"select * from webtoon_info where no={webtoon[0]}"))
        if(webtoon[1] == 'it'):
            it.append(db.query(webtoon_db,f"select * from webtoon_info where no={webtoon[0]}"))
        if(webtoon[1] == 'sv'):
            sv.append(db.query(webtoon_db,f"select * from webtoon_info where no={webtoon[0]}"))

    return render_template("recommend_page.html", dss = ds, its = it, svs = sv)

@auth.route("/get_rcm/<name>",methods=["GET"])
def get_rcm(name):
    #추천 결과
    no = db.query(webtoon_db,f"select no from webtoon_info where title='{name}'")
    surveys, drawings = models.main(name,no[0][0])

    #survey의 title로 webtoon넘버 가져오기
    surveys_no = []
    for name in surveys:
        surveys_no.append(db.query(webtoon_db,f"select no from webtoon_info where title='{name}'")[0][0])

    #추천 결과 history insert sql
    sql = "insert into history (user_id,webtoon_no,rcm_type) values "
    for survey in surveys_no:
        sql += f"('{session['user_id']}', {survey}, 'sv'),"
    for drawing in drawings:
        sql += f"('{session['user_id']}', {drawing}, 'ds'),"
    sql = sql[:-1]

    #history insert
    db.query(webtoon_db,sql)
    webtoon_db.commit()

    #가장 최근 날짜
    date = db.query(webtoon_db,f"select max(rcm_date) from history where user_id='{session['user_id']}'")

    return redirect(url_for("auth.recommend",date = date[0][0]))

# @auth.route("/recommend/<arg>",methods=["GET"])
# def recommend(arg):
#     print(arg)
#     return render_template("recommend_page.html")


@auth.route("/update_information",methods=["GET","POST"])
def upate_information():
    if request.method=="GET":
        return render_template("user_detail.html")
    elif request.method=="POST":
        id=session["user_id"]
        
        data=db.query(webtoon_db,f"SELECT password FROM user WHERE id='{id}'")
        print(data)
        check_password=data[0][0]
        print(check_password)
        print(request.form.get("password"))
        print(type(request.form.get("password")))
    
        if not request.form.get("password"):
            flash("비밀번호를 입력해주세요.",category="error")
            return render_template("user_detail.html")
        else:
            if check_password!=request.form.get("password"):
                flash("비밀번호가 틀립니다.",category="error")
                return render_template("user_detail.html")
            else:
                #update information
                update_name=request.form.get("name")
                update_gender=request.form.get("gender")
                update_age=request.form.get("age")
                
                if update_name==session["user_name"] and update_age==session["user_age"] and update_gender==session["user_gender"]:
                    flash("수정 할 내용이 없습니다.",category="error")
                    return render_template("user_detail.html")
                    
                db.query(webtoon_db,f"UPDATE user SET name='{update_name}', gender='{update_gender}', age='{update_age}' WHERE id='{id}'")

                #새로운 session 등록
                session.pop("user_name",None)
                session["user_name"]=update_name
                session.pop("user_gender",None)
                session["user_gender"]=update_gender
                session.pop("user_age",None)
                session["user_age"]=update_age
                webtoon_db.commit()
                flash("수정 완료되었습니다.",category="success")
                return render_template("user_detail.html")

#회원 탈퇴
@auth.route("/delete_user",methods=["POST"])
def delete_user():
    if request.method=="POST":
        if session:
            id=session["user_id"]
            data=db.query(webtoon_db,f"SELECT * FROM user WHERE id='{id}'")
            delete_user_data=data[0]    #('rlawogusWkd', 'QHFMADLWLQSOrJ', '김재현', '20대', 'male')
            print(delete_user_data)
            print(request.form.get("password"))
        
            if not request.form.get("password"):
                flash("비밀번호를 입력해주세요.")
                print("비밀번호를 입력해주세요.")
                return render_template("user_detail.html")
            else:
                if request.form.get("password")!=delete_user_data[1]:
                    print("비밀번호가 틀립니다.")
                    flash("비밀번호가 틀립니다.",category="error")
                    return render_template("user_detail.html")
                else:
                    session.pop("user_id",None)
                    session.pop("user_name",None)
                    session.pop("user_gender",None)
                    session.pop("user_age",None)
                    print(session)
                    db.query(webtoon_db,f"DELETE FROM user WHERE id='{id}'")
                    webtoon_db.commit()
                    flash("회원 탈퇴",category="success")
                    return redirect(url_for("views.index"))
        else:
            flash("로그인 되어 있지 않습니다.")
            return redirect(url_for("views.index"))

#정구리 작성 부분 => 별점 매기면 survey table 에 추가되는 페이지 !!!
# +------------+-------------+------+-----+---------+-------+
# | Field      | Type        | Null | Key | Default | Extra |
# +------------+-------------+------+-----+---------+-------+
# | user       | varchar(50) | NO   | PRI | NULL    |       |
# | webtoon_no | int         | NO   | PRI | NULL    |       |
# | score      | float       | NO   |     | NULL    |       |
# +------------+-------------+------+-----+---------+-------+
@auth.route("/input_rate",methods=["GET","POST"])
def input_rate():
    if session: #로그인 된 경우 (일단 안된 경우에는 return 되게 해놓기)
        if request.method =="GET": #get 인 경우에는 화면에 뿌려주기
            return render_template("input_rate.html")
        elif request.method =="POST":   
            user = session["user_id"] #세션의 유저 아이디를 user로
            title = request.form.get("title") #입력된 타이틀 명 가져오기 (select no from webtoon_info where title="마루는 강쥐";  통해서 webtoon_no 생성)
            score = request.form.get("score")

            webtoon_no = db.query(webtoon_db,f"SELECT no FROM webtoon_info WHERE title='{title}'") #이렇게하면 webtoon_no 반환
            print(user)
            print(webtoon_no[0][0])
            print("score = ",score)

            insert_to_survey = f"INSERT INTO survey VALUES ('{user}',{webtoon_no[0][0]},{score})"
            update_to_survey = f"UPDATE survey SET score={score} WHERE user='{user}' and webtoon_no={webtoon_no[0][0]};"
            
            try:
                check_insert = db.query(webtoon_db,insert_to_survey) #insert 문을 실행시킨다 만약 동일한 값이 있으면 except 로 이동
                webtoon_db.commit()
                flash("별점 등록 완료 !",category="success")
                return render_template("input_rate.html")
            except:
                update_survey = db.query(webtoon_db,update_to_survey) #만약 동일한 값이 있다면 기존 값을 수정하자 !!!
                webtoon_db.commit()
                flash("별점 등록 완료 !",category="success")
                return render_template("input_rate.html")

            
            
            

    else:

        flash("로그인 되어 있지 않습니다.",category="error")
        return redirect(url_for("views.index"))