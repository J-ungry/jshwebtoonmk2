#메인 Flask 서버 실행 -> main.py를 실행시켜야 서버가 켜짐
from website import init

app=init.create_app()

if __name__=="__main__": 
    app.run(debug=True)
    
"""
    *** 남은 해야할 일(221230) ***
    1. 최종 결과 페이지(로그인 안한 상태의 사용자는 따로 처리)
    2. 추천 알고리즘 정확도 높이기. 프로젝트 끝날 때 까지
    3. 설문조사 데이터 예외처리
    4. 기능 정의서 등 문서 작업
"""