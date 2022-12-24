#메인 Flask 서버 실행 -> main.py를 실행시켜야 서버가 켜짐
from website import init

app=init.create_app()

if __name__=="__main__": 
    app.run(debug=True)
    
"""
    *** 남은 해야할 일
    1. 전체적으로 css 다듬기
    2. user 아이디/비밀번호 변경 및 찾기
    3. introduce_service.html 완성
    4. 홈페이지에 들어갈 로고
    5. 키워드 들어간 웹툰 출력(input_keyword.html),키워드 검색 기능 추가 - 쿼리 고민
        => ajax는 되는데 결과가 바뀌지 않고 쌓임(무한 스크롤)
        => 줄거리 출력해야하고 (real_intro) 클릭시 다음 페이지로 이동하도록 a 태그로 생성하기
    6. 웹툰 모델 돌린 후 결과 페이지
    7. input_rate 자동완성 검색 기능 추가
    8. user_detail.html history 작성
    9. nav.html 상단바 선택 시 효과 추가
    10. 코드 정리
    11. 서비스소개 페이지 => 다른 페이지들 다 만들어진 이후에 사진 추가하기 (내용은 추가 된 상태임)
"""