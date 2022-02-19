from flask import Blueprint, render_template, request, flash, redirect, url_for # 한 파일에 뷰 여러개 안쑤셔박게해주는것
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash # u never save passwords in plain text. # but hashfunction = no inverse function exist.
from . import db
from flask_login import login_user, login_required, logout_user, current_user # usermixin 을 써넣은 이유임.

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first() # 같은 이메일 가진애를 찾아준다. # 만약 없다면,
        if user:
            if check_password_hash(user.password, password): # 해시함수를 통해 같은것을 확인했다면
                flash("... Logged in successfully...!", category = 'success')
                login_user(user, remember = True) # remembers the fact this user is logged in. (flask 세션에 기록이 쌓임.) # 계속 로그인 할 필요가 없음.
                return redirect(url_for('views.home'))
            else:
                flash("... Incorrect Password. Please Try Again ...!", category = 'error')
        else:
            flash("Email does not exist.", category = 'error')

    return render_template("login.html", user = current_user)


@auth.route('/logout')
@login_required # 로그인 안되있는데 로그아웃 할 수는 없다.
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category = 'error')
        elif len(email) < 4 :
            flash(" Email must be greater than 4 characters! ", category = 'error') # how do we alert users if things gone wrong? # message flashing 사용한다.
        elif len(first_name) < 2 :
            flash(" is your first name really 2 letters long?", category = 'error')
        elif password1 != password2 :
            flash(" Passwords don\'t match. ", category = 'error')
        elif len(password1) < 7 :
            flash(" Password must be greater than 7 characters! ", category = 'error')
        else:
            # add user to the database
            new_user = User(email = email,
                            first_name = first_name,
                            password = generate_password_hash(password1, method = 'sha256')) # models 에 넣어둔 유저에서 가져오는 거니까, .models 에서 user 를 임포트해와야함.
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash(" Account Created! ", category = 'success')
            return redirect(url_for('views.home')) # redirect to another page. # views.py 에 def.home 해놓은거 기억나지?

    return render_template("sign_up.html", user = current_user)
