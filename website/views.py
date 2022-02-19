from flask import Blueprint, render_template, request, flash, jsonify #blueprint 한 파일에 뷰 여러개 안쑤셔박게해주는것
from flask_login import login_required, current_user
from .models import Note
from . import db
import json


views = Blueprint('views', __name__)

@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get('note')

        if len(note) <= 1:
            flash("Note is too short.", category = 'error')
        else:
            new_note = Note(data = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category = 'success')

    return render_template("home.html", user = current_user) # current user 가 아니면 안해준다!


@views.route('/delete-note', methods = ['POST'])
def delete_note():
    note = json.loads(request.data) # json 으로 받은걸 dictionary 화 해준다고 생각하면 됨.
    noteId = note['note']
    note = Note.query.get(noteID)
    if note:
        if note.user_id == current_user.id: # 유저가 가진 노트가 맞으면 (일종의 security check)
            db.session.delete(note)
            db.session.commit()

    return jsonify({}) # 삭제한거임.
