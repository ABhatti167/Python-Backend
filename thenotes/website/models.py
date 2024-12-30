from . import db #imports db from the package( in init.py )
from flask_login import UserMixin #imports the sort of interface/abstratct class for the login details
from sqlalchemy.sql import func # imports a method to automatically set the datetime


class User(db.Model, UserMixin): # we use the UserMixin specifically for this
    id = db.Column(db.Integer, primary_key=True) # each user must have a primary key, i.e., a unique identifier
    email = db.Column(db.String(150), unique = True) # unique means no user can have the same email
    password = db.Column(db.String(150)) # 150 char limit
    firstName = db.Column(db.String(150))
    # the following is a list that stores user notes
    # NOTE: Unlike the foreign key method this will be capital as Note is capital(inconsistent)
    notes = db.relationship("Note") # What this does is to tell the db to add the notes id to user notes relationship
    
    
class Note(db.Model): #general schema for a note
    # NOTE: In general, when you define a new db object it automatically defines the id for you.
    # this id object is for learning purposes
    id = db.Column(db.Integer(), primary_key = True)
    
    content = db.Column(db.String(1500))
    date = db.Column(db.DateTime(timezone=True), 
                     default= func.now())
    # key to keep track of its corresponding user, one to many relationship as a user can have multiple notes
    # the foreign key is defined in the child object to refer to the parent
    # in SQL User will be referred to as user, and the key can be any part of the user like email, id whatever
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # specifies the id of the user who made the note, integer column
    