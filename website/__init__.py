from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"



def create_app():

    app = Flask(__name__) # __name__ 파일의 이름을 지정함. 별 설명은 안하고 넘어감.
    app.config['SECRET_KEY'] = 'january' # initialize secret key.
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # 해당 로케에 있다는 것을 의미함.
    db.init_app(app)


    from .views import views # views.py 의 views 함수 임포트
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/') # url_prefix 로 '/hello/' 로 설정한다면
    app.register_blueprint(auth, url_prefix = '/') # 그 쪽으로 가는 url 앞에는 /hello/... 이렇게 붙음.

    from .models import User, Note # cant reference since you cant start variable name with a dot.
    create_database(app) # create a database.

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # telling flask how do we load the user. by default we look at int(id) PK check.

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME): # website/ 의 db 있는지 체크
        db.create_all(app = app) # 없으면 만들고
        print('... Created Database ...')



