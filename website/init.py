from typing import TYPE_CHECKING
from flask import Flask


def create_app():
    app=Flask(__name__)
    app.config["SECRET_KEY"]="sdjisnoafsada"    #비밀키인데 의미 없음. 바꾸지 마세요.
    
    #Blueprint 등록 -> 이거 안되면 route에서 url 못 받아옴
    from .views import views
    from .auth import auth
    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/")
    
    return app