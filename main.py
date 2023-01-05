#메인 Flask 서버 실행
from website import init

app=init.create_app()

if __name__=="__main__": 
    app.run(debug=True)