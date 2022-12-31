from flask import Blueprint,render_template,session,request,jsonify,flash,redirect,url_for
from website import db,models,auth,views

views = Blueprint("views",__name__)

@views.route("/")
def index():
    return render_template("index.html")

@views.route("/introduce_service")
def introduce_service():
    return render_template("introduce_service.html")

@views.route("/introduce_team")
def introduce_team():
    return render_template("introduce_team.html")

#코드 수정해야돼,,
@views.route("/input_keyword",methods=["GET","POST"])
def input_keyword():
    if request.method=="GET":
        #장르 = genre, 소재=sojae, 분위기 = atm, 수상작 = soosang, 등장인물/관계 = charel, 원작웹툰 = origin
        if session:
            return_genre=[] 
            return_sojae=[]
            return_atm=[]
            return_soosang=[]
            return_chrel=[]
            return_origin=[]
            return_title=[]
        
            try:
                webtoon_db = db.conn()
                try:
                    #장르 = 1 소재 = 2 분위기 = 3 수상작 = 4 등장인물관계 = 5 원작웹툰 =6 
                    for type in range(1,7):
                        datas=db.select_query(webtoon_db,f"SELECT DISTINCT keyword FROM keyword WHERE type='{type}' ORDER BY keyword")
                        if type==1:
                            genre=datas
                        elif type==2:
                            sojae=datas
                        elif type==3:
                            atm=datas
                        elif type==4:
                            soosang=datas
                        elif type==5:
                            chrel=datas
                        else:
                            origin=datas
                    
                    data=db.select_query(webtoon_db,f"SELECT title FROM webtoon_info")

                    for i in range(len(data)):
                        return_title.append(data[i][0])
                    
                    for i in range(len(genre)):
                        return_genre.append(genre[i][0])
                        
                    for i in range(len(sojae)):
                        return_sojae.append(sojae[i][0])
                        
                    for i in range(len(atm)):
                        return_atm.append(atm[i][0])
                    
                    for i in range(len(soosang)):
                        return_soosang.append(soosang[i][0])
                    
                    for i in range(len(chrel)):
                        return_chrel.append(chrel[i][0])
                    
                    for i in range(len(origin)):
                        return_origin.append(origin[i][0])
                    
                    return render_template("input_keyword.html",genre=return_genre,sojae=return_sojae,atm=return_atm,soosang=return_soosang,chrel=return_chrel,origin=return_origin,titles=return_title)
                except:
                    flash("execute error",category="error")
                    return redirect(url_for("/input_keyword"))
                finally:
                    webtoon_db.close()
            except:
                #DB 에러 발생 시 실행되는 코드
                flash("DB connect error",category="error")
                return redirect(url_for("/input_keyword"))
    
    elif request.method=="POST":    #키워드 결과 ajax
        keyword=request.form["keyword"]             #6
        keyword_user=request.form["user_keyword"]   #2017 최강자전
        
        return_webtoon_data=[]    #html에 넘길 웹툰 데이터
        return_webtoon_title=[]
        return_webtoon_thumb=[]
        return_webtoon_author=[]
        return_webtoon_intro=[]
        
        try:
            webtoon_db = db.conn()
            try:
                #사용자가 선택한 키워드가 있는 웹툰 번호 출력
                keyword_webtoon_no_data=db.select_query(webtoon_db,f"SELECT no FROM keyword WHERE keyword IN('{keyword_user}') AND type='{keyword}'")
                
                for i in range(len(keyword_webtoon_no_data)):
                    return_webtoon_data=db.select_query(webtoon_db,f"SELECT title,author,thumb_link,real_intro FROM webtoon_info WHERE no='{keyword_webtoon_no_data[i][0]}'")
                    return_webtoon_title.append(return_webtoon_data[0][0])
                    return_webtoon_author.append(return_webtoon_data[0][1])
                    return_webtoon_thumb.append(return_webtoon_data[0][2])
                    return_webtoon_intro.append(return_webtoon_data[0][3])

                return jsonify({"keyword":keyword,"user_keyword":keyword_user,"webtoon_title":return_webtoon_title,"webtoon_author":return_webtoon_author,"webtoon_thumb":return_webtoon_thumb,"webtoon_intro":return_webtoon_intro})
            except:
                flash("execute error",category="error")
                return redirect(url_for("/input_keyword"))
            finally:
                webtoon_db.close()

        except:
            #DB 에러 발생 시 실행되는 코드
            flash("DB connect error",category="error")
            return redirect(url_for("/input_keyword"))

#웹툰명 자동완성
@views.route("/autocomplete",methods=["POST"])
def autocomplete():
    val = request.form["value"]
    
    try:
        webtoon_db = db.conn()
        try:
            resultList = db.select_query(webtoon_db,f"select title from webtoon_info where title like '%{val}%'")
            titleList = []
            for result in resultList:
                titleList.append(result[0])

            return jsonify({"titleList":titleList})
        except:
            flash("execute error",category="error")
            return redirect(url_for("views.index"))
        finally:
            webtoon_db.close()
    except:
        #DB 에러 발생 시 실행되는 코드
        flash("DB connect error",category="error")
        return redirect(url_for("views.index"))


# 키워드 검색 자동완성 리스트
@views.route("/keyword_autocomplete",methods=["POST"])
def keyword_autocomplete():
    val=request.form["value"]

    try:
        webtoon_db = db.conn()
        try:
            resultList = db.select_query(webtoon_db,f"SELECT DISTINCT keyword FROM keyword WHERE keyword like '%{val}%'")

            # 검색한 키워드가 리스트로 저장됨
            keywordList = []
            for result in resultList:
                keywordList.append(result[0])
            return jsonify({"keywordList":keywordList})
        except:
            flash("execute error",category="error")
            return redirect(url_for("views.index"))
        finally:
            webtoon_db.close()
    except:
        #DB 에러 발생 시 실행되는 코드
        flash("DB connect error",category="error")
        return redirect(url_for("views.index"))

# 검색한 키워드 추가
@views.route("/addAutoCompleteKeyword",methods=["POST"])
def addSearchedKeyword():
    # AJAX 통신 확인
    print("WOW AJAX!🌟")
    try:
        webtoon_db = db.conn()
        try:
            query_result = db.select_query(webtoon_db,f"SELECT DISTINCT keyword FROM keyword")
            all_keyword_list = []
            for result in query_result:
                all_keyword_list.append(result[0])

            inputValue = request.form["inputValue"]
            print("inputValue 키워드 검색창에 입력한 값 = ", inputValue)

            # 키워드 검색창에 입력한 값이 DB에 있나요?
            if (inputValue in all_keyword_list):
                # DB에 있어요 ^^b
                existInDB = True
                print(existInDB, '검색한 키워드가 DB에 있어요✨')
            else:
                # DB에 없어요 ㅠㅠ
                existInDB = False
                print(existInDB, '검색한 키워드가 DB에 없어요💥')
            
            if(existInDB):
                # 검색한 키워드가 DB에 존재하면 실행

                return_webtoon_data=[]    #html에 넘길 웹툰 데이터
                return_webtoon_title=[]
                return_webtoon_thumb=[]
                return_webtoon_author=[]
                return_webtoon_intro=[]

                # 검색한 키워드의 type 번호가 무엇인가요?
                autoCompleteKeyword_num_db_data = db.select_query(webtoon_db,
                f"SELECT DISTINCT type FROM keyword WHERE keyword='{inputValue}'")
                autoCompleteKeyword_num = autoCompleteKeyword_num_db_data[0][0]
                print("autoCompleteKeyword_num :", autoCompleteKeyword_num)

                # 검색한 키워드와 type 번호가 일치하는 웹툰들은 무엇인가요?
                autoCompleteKeyword_webtoon_no_db_data=db.select_query(webtoon_db,
                f"SELECT no FROM keyword WHERE keyword IN('{inputValue}') AND type='{autoCompleteKeyword_num}'")
                print("autoCompleteKeyword_webtoon_no_db_data :", autoCompleteKeyword_webtoon_no_db_data)

                for i in range(len(autoCompleteKeyword_webtoon_no_db_data)):
                    return_webtoon_data=db.select_query(webtoon_db,
                    f"""
                    SELECT title, author, thumb_link, real_intro 
                    FROM webtoon_info 
                    WHERE no='{autoCompleteKeyword_webtoon_no_db_data[i][0]}'
                    """)
                    return_webtoon_title.append(return_webtoon_data[0][0])
                    return_webtoon_author.append(return_webtoon_data[0][1])
                    return_webtoon_thumb.append(return_webtoon_data[0][2])
                    return_webtoon_intro.append(return_webtoon_data[0][3])
                
                for i in range(len(return_webtoon_title)):
                    print(return_webtoon_title[i])
                
                return jsonify({
                    "existInDB" : existInDB,                 # 검색한 키워드의 DB 존재 유무
                    "inputValue" : inputValue,               # 검색한 키워드 문자
                    "keyword_type": autoCompleteKeyword_num, # 검색한 키워드의 type 번호
                    "webtoon_title":return_webtoon_title,    # 검색한 키워드의 웹툰 제목
                    "webtoon_author":return_webtoon_author,  # 검색한 키워드의 웹툰 작가
                    "webtoon_thumb":return_webtoon_thumb,    # 검색한 키워드의 웹툰 썸네일
                    "webtoon_intro":return_webtoon_intro     # 검색한 키워드의 웹툰 줄거리
                    })
                
            else:
                # 검색한 키워드가 DB에 존재하면 실행
                return jsonify({
                    "existInDB" : existInDB, 
                    "inputValue" : inputValue
                    })
        except:
            flash("execute error",category="error")
            return redirect(url_for("views.index"))
        finally:
            webtoon_db.close()
    except:
        #DB 에러 발생 시 실행되는 코드
        flash("DB connect error",category="error")
        return redirect(url_for("views.index"))
