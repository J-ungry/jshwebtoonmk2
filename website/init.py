from typing import TYPE_CHECKING
from flask import Flask
from flask_mail import Mail

def create_app():
    
    global app
    app=Flask(__name__)
    app.config["SECRET_KEY"]="sdjisnoafsada"    #비밀키인데 의미 없음. 바꾸지 마세요.
    
    #Blueprint 등록 -> 이거 안되면 route에서 url 못 받아옴
    from .views import views
    from .auth import auth
    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/")
    #session 등록하기 위해서는 필수. 생략 안됨
    app.secret_key="kth"
    
    return app


def create_mail():

    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USERNAME"] = "webtoonroomnoreply@gmail.com"
    app.config["MAIL_PASSWORD"] = "vpuljlbkjtcubkqo"
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True

    email = Mail(app)

    return email