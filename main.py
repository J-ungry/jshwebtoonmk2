#메인 Flask 서버 실행 -> main.py를 실행시켜야 서버가 켜짐
from website import init

app=init.create_app()

if __name__=="__main__": 
    app.run(debug=True)


#재현mk2