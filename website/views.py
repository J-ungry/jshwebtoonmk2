from flask import Blueprint,render_template,session,request,jsonify
from website import db,models,auth

webtoon_db=auth.webtoon_db  #db연결
views = Blueprint("views",__name__)

@views.route("/")
def index():
    return render_template("index.html",)

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
        
            #장르 = 1 소재 = 2 분위기 = 3 수상작 = 4 등장인물관계 = 5 원작웹툰 =6 
            for type in range(1,7):
                datas=db.query(webtoon_db,f"SELECT DISTINCT keyword FROM keyword WHERE type='{type}' ORDER BY keyword")
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
                    
            print(genre)
            
            data=db.query(webtoon_db,f"SELECT title FROM webtoon_info")
            print(len(data))
            
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
                
            # result,dsModel=models.main()
            # print(result)
            # print(dsModel)
            
            return render_template("input_keyword.html",genre=return_genre,sojae=return_sojae,atm=return_atm,soosang=return_soosang,chrel=return_chrel,origin=return_origin,titles=return_title)
    
    elif request.method=="POST":
        keyword_test=request.form["keyword"]
        keyword_user=request.form["user_keyword"]
        print(keyword_test)
        print(keyword_user)
        model_result=models.main(keyword_user)
        print(model_result)
        return jsonify({"keyword":keyword_test,"user_keyword":keyword_user,"model_result":model_result})
    