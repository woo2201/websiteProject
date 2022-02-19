from . import db # current folder 에서 db 를 import 한다 (init 의 db를 불러온다는 것)
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True), default = func.now()) # 오늘 날짜로 default setitng.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # oneTomany 이슈? 한사람이 노트 여러개.
                                                              # user.id 일때 왜 user 를 lower case?
                                                              # 이건 sql 에서 그리하기 때문이라고 함. 클래스User에서 가져온거맞음.
                                                              # foreign 키란, 다른 데이터베이스와 엮을 수 있는 키를 말함. (한국어로는 외래키였던거 같음.)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True) # pk 로 설정
    email = db.Column(db.String(150), unique = True) # no same email allowed.
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') # everytime you create a note, user에 note 에 대한 아이디를 저장한다. # 여기는 왜 lowercase 가 아니냐고? way it is. 포린키는 그대로.

