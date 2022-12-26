from matplotlib.pyplot import get
import numpy as np 
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from website import db,auth

from numpy import dot
from numpy.linalg import norm

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

    #유사도 상위 5개 웹툰번호 return
    df = pd.DataFrame(sim, columns=['sim'])
    return df.sort_values('sim', ascending=False)[1:6].index + 1

#승환이코드

def itModel(wt_title):
    num = 5

    fake_intro = db.query(webtoon_db, "SELECT fake_intro FROM webtoon_info")

    transformer = TfidfVectorizer()
    tfidf_matrix = transformer.fit_transform(fake_intro)
    print(tfidf_matrix.shape) #(1000, 9662)

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    print(cosine_sim.shape) #(2044, 2044)

    # webtoon_info to dataframe
    column = ['no', 'title', 'link', 'thumb_link', 'status', 'author', 'fake_intro', 'real_intro','likes', 'episodes', 'first_register_date', 'last_register_date', 'age','rate', 'genre1_pre', 'genre2_pre']
    datas = db.query(webtoon_db,"select * from webtoon_info")
    webtoon_data = pd.DataFrame(datas,columns=column)

    # 선택한 웹툰의 title로부터 해당되는 인덱스를 받아옵니다. 이제 선택한 웹툰를 가지고 연산할 수 있습니다.
    indices = pd.Series(webtoon_data.index, index=webtoon_data['title'])
    idx = indices[wt_title]

    # 모든 웹툰에 대해서 해당 웹툰과 유사도를 구합니다.
    sim_scores = cosine_sim[idx]
    sim_scores = list(enumerate(sim_scores))

    # 유사도에 따라 웹툰을 정렬합니다.
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 가장 유사한 num개의 웹툰를 받아옵니다.
    sim_scores = sim_scores[1:num+1]

    # 가장 유사한 5개의 영화의 인덱스를 받아옵니다.
    webtoon_indices = [i[0] for i in sim_scores]
    recommended_it_lists = webtoon_data['title'].iloc[webtoon_indices].to_list()
    print(recommended_it_lists) # ['오직 나의 주인님', '개를 낳았다', '토니와 함께', '그 개, 만두', '언럭키 맨션']

    return recommended_it_lists




def main(title,no):
    survey = recommand_webtoon(title)
    drawing = dsModel(no)

    return survey, drawing

# if __name__ =='__main__':
#     main()