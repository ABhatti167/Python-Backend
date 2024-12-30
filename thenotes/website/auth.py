from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash #allows creating/scanning of hashes
from . import db
from flask_login import login_user, login_required, logout_user, current_user # tracks current user info, currnt user requires UserMixin
import json # for js communcation

# define this file as a blueprint, meaning it contains routes

auth = Blueprint('auth', __name__)

@auth.route('login', methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first() # returns queried user
        
        if user: # if we obtain a user with such email
            if check_password_hash(user.password, password): # if the password is equal to whats entered
                flash ('Logged in successfully!', category='success')
                login_user(user, remember=True) # logs in user and remembers it until sesseion/history cleared
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect credentials', category='fail')
        else:
            flash('Email does not exist.', category='error')
                
    
    return render_template("login.html", 
                           user = current_user)

@auth.route('logout')
@login_required # we use this to make sure that the logout option cannot be accessed unless signed in.
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("signup", methods=["GET", "POST"]) # can define arg to enable http methods
def sign_up():
    # request object obtains http request info including what data is passed to it
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first() # returns queried user

        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstName) < 2:
            flash("First Name must be greater than 1 characters.", category='error')
        elif password1 != password2:
            flash("Passwords do not match.", category="error")
        elif len(password1) < 7:
            flash("Password must be greater than 7 characters.", category="error")
        else:
            # create new user for db
            new_user = User(
                email=email,
                firstName=firstName,
                password=generate_password_hash(password1, method="pbkdf2:sha256"),
            )

            db.session.add(new_user) # adds user to db
            db.session.commit() # commit changes
            login_user(new_user, remember=True) # logs in user and remembers it until sesseion/history cleared

            flash("Added new user.", category="success")

            return redirect(url_for('views.home')) # since views is a different file

    return render_template("signup.html", user = current_user)
