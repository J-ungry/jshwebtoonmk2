from matplotlib.pyplot import get
import numpy as np 
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from website import db,auth

from numpy import dot
from numpy.linalg import norm

webtoon_db=auth.webtoon_db

def make_list(datas):
    lst = []
    for i in datas:
        lst.append(i[0])
    return lst

#데이터 호출함수=> 추후 DB 에서 호출하게끔 개선하기 (완료)
def get_data():

    #webtoon_info to dataframe
    datas = db.query(webtoon_db,"select column_name from information_schema.columns where table_name='webtoon_info'")
    column = ['no', 'title', 'link', 'thumb_link', 'status', 'author', 'fake_intro', 'real_intro','likes', 'episodes', 'first_register_date', 'last_register_date', 'age','rate', 'genre1_pre', 'genre2_pre']
    
    datas = db.query(webtoon_db,"select * from webtoon_info")
    webtoon_data = pd.DataFrame(datas,columns=column)
    
    #survey to dataframe 
    datas = db.query(webtoon_db,"select column_name from information_schema.columns where table_name='survey'")
    column = ['user', 'webtoon_no', 'score']

    datas = db.query(webtoon_db,"select * from survey")
    rating_data = pd.DataFrame(datas,columns=column)
    
    return rating_data,webtoon_data

# -정구리- 협업필터링
#데이터 전처리
def preprocessing_data(rating_data,webtoon_data):

    #merge, drop (no 기준으로 merge)
    dic_corr = dict(enumerate(webtoon_data['title'],start=1))
    
    rating_data['title'] = rating_data['webtoon_no'].map(dic_corr)

    #make pivot
    usr_webtoon_pivot = rating_data.pivot_table('score',index="user",columns='title')

    #NaN -> 0.0 SVD 동작을 위해선 Nan 형태가 있으면 안된덩 ㅋㅋ
    usr_webtoon_pivot = usr_webtoon_pivot.fillna(0)
    
    #column <-> row
    webtoon_usr_pivot = usr_webtoon_pivot.values.T
    webtoon_usr_pivot.shape

    webtoon_title = usr_webtoon_pivot.columns

    return webtoon_usr_pivot,webtoon_title

def truncateSVD(rating_data,webtoon_data):
    webtoon_usr_pivot,webtoon_title  = preprocessing_data(rating_data,webtoon_data)
    #임의의 12개의 조건 생성
    SVD = TruncatedSVD(n_components=12) 
    matrix = SVD.fit_transform(webtoon_usr_pivot)

    corr = np.corrcoef(matrix)

    return corr,webtoon_title

def recommand_webtoon(title):
    result = [] #최종 결과 들어갈 list
    rating_data,webtoon_data = get_data() #데이터 호출하기 
    corr,webtoon_title = truncateSVD(rating_data,webtoon_data) #model 에 돌리기 
    webtoon_title_list = list(webtoon_title) #웹툰 제목 호출하기
    target = webtoon_title_list.index(title) #입력받은 웹툰의 index
    corr_target = corr[target]
    
    #딕셔너리로 바꾼 뒤에 상위 5개만 출력 + 자기 자신 제외하기
    dic_corr = dict(enumerate(corr_target))
    dic_corr = list(dict(sorted(dic_corr.items(),key=lambda item:item[1],reverse=1)).keys())[:6] #6인 이유는 자기자신 제외를 위해
    for i in dic_corr:
        result.append(webtoon_title[i])
    return result[1:]

#재현이소스

#코사인 유사도
def cos_sim(A, B):
    return dot(A, B)/(norm(A)*norm(B))

def dsModel(webtoon_no):

    #이미지 특징 vector select
    tup = db.query(webtoon_db,"select resnet from thumb")

    vec = []
    for y in range(len(tup)):
        vec.append(eval(tup[y][0]))

    #유사도 계산
    sim = []
    for x in range(0,2044):
        sim.append(cos_sim(vec[webtoon_no-1],vec[x]))

    #유사도 상위 10개 웹툰번호 return
    df = pd.DataFrame(sim, columns=['sim'])
    return df.sort_values('sim', ascending=False)[:5].index + 1


def main(title,no):
    survey = recommand_webtoon(title)
    drawing = dsModel(no)

    return survey, drawing

# if __name__ =='__main__':
#     main()