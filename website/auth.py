from flask import Blueprint,render_template,request,flash,redirect,url_for,session
from werkzeug.security import generate_password_hash,check_password_hash
from website import db
import pymysql
import website.models as models
import string
import secrets
from flask_mail import Mail, Message
from website import init

"""
    **1228 예외처리 시작
    1. DB 연결 관한 예외처리
        로그인 같은 경우 유효성 검사 후에만 쿼리 호출 => 그 후 작업이 끝나면 db.close()
        finally로 넣지마세요.
    2. 한번만 쓰는 변수는 삭제했습니다.
    3. 테스트 후 print는 거의 삭제하겠습니다.
"""

# DB_USER="jsh"   #MySQL 계정명
# #DB_USER = "root" #정구리 MySQL 계정명
# DB_NAME="jsh"   #MySQL DB명

#auth.py에서는 주로 로그인에 관련된 코드 작성
auth = Blueprint("auth",__name__)

webtoon_db = pymysql.connect(   
        host="localhost",
        port=3306,
        user=db.DB_USER,
        #passwd="bread!123",
        passwd="duffufK123!",
        db=db.DB_NAME,
        charset="utf8"
        )
print("connect MySQL🎉")

#로그인

@auth.route("/user_login",methods=["GET","POST"])
def user_login():
    if request.method=="GET":
        return render_template("login.html")
    elif request.method=="POST":
        id=request.form.get("id")
        password=request.form.get("password")
        
        #유효성 검사는 js로 대체예정, 아이디와 비밀번호가 모두 입력 되었을 때만 쿼리 호출로 수정
        if len(id)<1:
            flash("아이디를 입력하세요.",category="error")
            #return redirect(url_for("auth.user_login"))
            return render_template("login.html")
        else:
            if len(password)<1:
                flash("비밀번호를 입력하세요.",category="error")
                return render_template("login.html")
            else:
                try:
                    select_user=db.query(webtoon_db,f"SELECT * FROM user WHERE id='{id}'")
                    # 해당 id에 해당하는 정보가 있을 경우
                    if select_user:
                        login_user_check=select_user[0]
                        login_user_password=login_user_check[1]
                
                        if not check_password_hash(login_user_password, password):
                            flash("비밀번호가 틀립니다.",category="error")
                            return redirect(url_for("auth.user_login"))
                        else:
                            #session에서 id는 user_id,name은 user_name,age는 user_age,gender는 user_gender
                            session["user_id"]=id
                            session["user_name"]=login_user_check[2]
                            session["user_email"]=login_user_check[3]
                            session["user_age"]=login_user_check[4]
                            session["user_gender"]=login_user_check[5]
                            flash("로그인 성공",category="success")
                            #webtoon_db.close() 조심
                            webtoon_db.close()
                            return redirect(url_for("views.index"))
                    else:
                        flash("아이디가 존재하지 않습니다.",category="error")
                        return redirect(url_for("auth.user_login"))    
                except:
                    #DB 에러 발생 시 실행되는 코드
                    flash("다시 로그인 하세요.",category="error")
                    return redirect(url_for("auth.user_login"))


#회원가입

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
        email=request.form.get("email")
        
        #각 input 입력 했을 때만 쿼리 호출, 유효성 검사는 js로 대체
        if len(id)<5:
            flash("아이디는 5글자 이상입니다.",category="error")
            return render_template("sign_up.html")
        else:
            if len(name)<1:
                flash("이름을 입력하세요.",category="error")
                return render_template("sign_up.html")
            else:
                if len(password)<1:
                    flash("비밀번호를 입력하세요.",category="error")
                    return render_template("sign_up.html")
                elif len(password)<7:
                    flash("비밀번호가 너무 짧습니다.",category="error")
                    return render_template("sign_up.html")
                elif password != repassword:
                    flash("재확인 비밀번호를 다시 입력해주세요.",category="error")
                    return render_template("sign_up.html")
                else:
                    if gender=="else":
                        flash("성별을 선택해주세요.",category="error")
                        return render_template("sign_up.html")
                    elif age=="else":
                        flash("연령대를 선택해주세요.",category="error")
                        return render_template("sign_up.html")
                    else:
                         #check_id 값이 없을 경우 에러처리
                        try:
                            check_id=db.query(webtoon_db,f"SELECT id FROM user WHERE id='{id}'")
                            if check_id:
                                flash("이미 존재하는 아이디입니다.",category="error")
                                return redirect(url_for("auth.user_login"))
                            else:
                                pw = generate_password_hash(password)
                                try:
                                    insert_user_data=f"INSERT INTO user VALUES ('{id}','{pw}','{name}','{email}','{age}','{gender}')"
                                    check=db.query(webtoon_db,insert_user_data)           
                                    webtoon_db.commit()
                                    flash("회원가입 완료.",category="success")
                                    webtoon_db.close()
                                    return redirect(url_for("views.index"))
                                except:
                                    #insert 에러 처리
                                    flash("다시 시도해주세요.",category="error")
                                    return redirect("sign_up.html")
                        except:
                            #DB에러가 발생했을 때 처리
                            flash("다시 시도해주세요.",category="error")
                            return redirect("sign_up.html")

#로그아웃
@auth.route("/logout",methods=["GET"])
def logout():
    if request.method=="GET": 
        if session:
            #session에 등록되어 있는 정보 삭제
            session.pop("user_id",None)
            session.pop("user_name",None)
            session.pop("user_age",None)
            session.pop("user_gender",None)
            session.pop("user_email",None)
            flash("로그아웃되었습니다.",category="success")
            return render_template("index.html")
        else:
            flash("로그인 한 유저만 사용할 수 있습니다.",category="error")
            return redirect(url_for("views.index"))
    elif request.method=="POST":
        flash("잘못된 접근입니다.",category="error")
        return redirect(url_for("views.index"))

#마이페이지. 여기서는 webtoon_db.close() 쓰지마세요.
@auth.route("/user_detail",methods=["GET"])
def user_detail():
    if request.method=="GET":
        if session:
            try:
                dates=db.query(webtoon_db,f"select DISTINCT rcm_date from history where user_id='{session['user_id']}' order by rcm_date desc")
                return render_template("user_detail.html", dates = dates)
            except:
                flash("다시 시도하세요.",category="error")
                return redirect(url_for("views.index"))
        else:
            flash("해당 서비스는 로그인 한 사용자만 이용가능합니다.",category="error")
            return redirect(url_for("views.index"))
    elif request.method=="POST":
        flash("잘못된 접근입니다.",category="error")
        return redirect(url_for("views.index"))


#회원정보 수정

@auth.route("/update_information",methods=["GET","POST"])
def update_information():
    if request.method=="GET":
        return redirect("/user_detail")
    elif request.method=="POST":
        id=session["user_id"]
        if not request.form.get("password"):
            flash("비밀번호를 입력해주세요.",category="error")
            return redirect("/user_detail")
        else:
            data=db.query(webtoon_db,f"SELECT password FROM user WHERE id='{id}'")
            check_password=data[0][0]
            
            if not check_password_hash(check_password,request.form.get("password")):
                flash("비밀번호가 틀립니다.",category="error")
                return redirect("/user_detail")
            else:
                #update information
                update_name=request.form.get("name")
                update_gender=request.form.get("gender")
                update_age=request.form.get("age")
                update_email=request.form.get("email")
                update_new_pw=request.form.get("new_pw")
                update_new_pw_check=request.form.get("new_pw_check")
                
                if update_name==session["user_name"] and update_age==session["user_age"] and update_gender==session["user_gender"] and update_email==session["user_email"] and check_password_hash(check_password, update_new_pw):
                    flash("수정 할 내용이 없습니다.",category="error")
                    return redirect("/user_detail")

                #-------------------------------유효성검사 후 삭제
                if update_new_pw != update_new_pw_check:
                    flash("새 비밀번호 확인값이 다릅니다.",category="error")
                    return redirect("/user_detail")
                #-------------------------------

                hashed_new_pw = generate_password_hash(update_new_pw)
                db.query(webtoon_db,f"UPDATE user SET name='{update_name}', gender='{update_gender}', age='{update_age}', email='{update_email}', password='{hashed_new_pw}' WHERE id='{id}'")

                #새로운 session 등록
                session.pop("user_name",None)
                session["user_name"]=update_name
                session.pop("user_gender",None)
                session["user_gender"]=update_gender
                session.pop("user_age",None)
                session["user_age"]=update_age
                session.pop("user_email",None)
                session["user_email"]=update_email
                webtoon_db.commit()
                flash("수정 완료되었습니다.",category="success")
                return redirect("/user_detail")

#회원 탈퇴
@auth.route("/delete_user",methods=["POST"])
def delete_user():
    if request.method=="POST":
        if session:
            id=session["user_id"]
            data=db.query(webtoon_db,f"SELECT * FROM user WHERE id='{id}'")
            delete_user_data=data[0] 
        
            if not request.form.get("password"):
                flash("비밀번호를 입력해주세요.")
                return render_template("user_detail.html")
            else:
                if not check_password_hash(delete_user_data[1],request.form.get("password")):
                    flash("비밀번호가 틀립니다.",category="error")
                    return render_template("user_detail.html")
                else:
                    session.pop("user_id",None)
                    session.pop("user_name",None)
                    session.pop("user_gender",None)
                    session.pop("user_age",None)
                    session.pop("user_email",None)
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

#김재현 작성 부분

# 아이디 찾기
@auth.route("/find_id",methods=["POST"])
def find_id():
    name=request.form.get("name")
    email=request.form.get("email")

    #-------------------
    if name == "" or email == "":
        flash("존재하지 않는 정보입니다!",category="error")
        return render_template("login.html")
    #-------------------js로 유효성 검사 후 삭제

    id = db.query(webtoon_db,f"select id from user where email = '{email}' and name = '{name}'")

    if len(id) == 0:
        flash("존재하지 않는 정보입니다!",category="error")
        return render_template("login.html")

    return render_template("find_id.html", id=id[0][0])

@auth.route("/reset_pw",methods=["POST"])
def reset_pw():
    name=request.form.get("name")
    email=request.form.get("email")
    id=request.form.get("id")

    #-------------------
    if name == "" or email == "" or id == "":
        flash("존재하지 않는 정보입니다!",category="error")
        return render_template("login.html")
    #-------------------js로 유효성 검사 후 삭제

    user = db.query(webtoon_db,f"select * from user where email = '{email}' and name = '{name}' and id = '{id}'")

    if len(user) == 0:
        flash("존재하지 않는 정보입니다!",category="error")
        return render_template("login.html")

    #임시 비밀번호 생성
    alphabet = string.ascii_letters + string.digits
    new_pw = ''.join(secrets.choice(alphabet) for x in range(8))

    #db에서 임시비밀번호로 변경
    hashed_pw = generate_password_hash(new_pw)
    db.query(webtoon_db,f"update user set password = '{hashed_pw}' where id = '{id}'")
    webtoon_db.commit()
    
    #메일로 발송
    msg = Message(
        "jsh's comic room temporary password",
        body=new_pw,
        sender="webtoonroomnoreply@gmail.com",
        recipients=[email]
    )
    email_lib = init.create_mail()
    email_lib.send(msg)

    flash("임시비밀번호를 메일로 발송하였습니다.",category="success")
    return redirect(url_for('auth.user_login'))


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
    surveys, drawings,intros = models.main(name,no[0][0])

    #survey의 title로 webtoon넘버 가져오기
    surveys_no = []
    for name in surveys:
        surveys_no.append(db.query(webtoon_db,f"select no from webtoon_info where title='{name}'")[0][0])

    #intro의 title 로 webtoon넘버 가져오기 (이렇게 하면 되나 ???)
    intros_no = []
    for x in intros:
        intros_no.append(db.query(webtoon_db,f"select no from webtoon_info where title='{x}'")[0][0])

    #추천 결과 history insert sql
    sql = "insert into history (user_id,webtoon_no,rcm_type) values "
    for survey in surveys_no:
        sql += f"('{session['user_id']}', {survey}, 'sv'),"
    for drawing in drawings:
        sql += f"('{session['user_id']}', {drawing}, 'ds'),"
    for intro in intros_no:
        sql += f"('{session['user_id']}', {intro}, 'it'),"
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

