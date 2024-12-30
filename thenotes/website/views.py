from flask import Blueprint, render_template, jsonify
from flask import request, flash
import time
from .models import Note
from . import db
from flask_login import (
    login_user,
    login_required,
    logout_user,
    current_user,
)  # tracks current user info, currnt user requires UserMixin
import json

# define this file as a blueprint, meaning it contains routes

views = Blueprint('views', __name__)

# @blueprintname,route(url)
@views.route('/', methods=["GET", "POST"])
@login_required # cannot be accessed unless signed in.
def home(): #run when route is run
    if request.method == "POST":

        content = request.form.get("note")
        
        if len(content) > 0:
            flash("Note Made.", category="success")
            new_note = Note(content = content, user_id = current_user.id)

            db.session.add(new_note)
            db.session.commit()
        else:
            flash("Invalid Message", category='error')

    return render_template(
        "home.html", user = current_user)

@views.route('/delete-note', methods = ['POST'])
def delete_note():
    note = json.loads(request.data) #loads note data as dictionary
    noteId = note['noteId'] # we access the id of note
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({}) # its a requirement to return this