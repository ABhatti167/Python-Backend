from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager # actually keeps track of logged in users.

db = SQLAlchemy() #initialize new db object
DB_NAME = "database.db" # by convention .db

def create_app() -> Flask:
    app = Flask(__name__) # init the app

    # set the key to store all data(cookies, data)
    app.config["SECRET_KEY"] = 'my_key' # can be anything

    # NOTE: Configure the db settings prior to creating db

    # says the db should be stored at the location on rhs
    # stores db in website folder of init.py
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # app will connect with the db
    db.init_app(app)

    # register blueprints
    from .views import views
    from .auth import auth

    # register it with app and make it
    # accessible using the prefix

    # since we have say /auth/ we need to do /auth/(pagename)
    # to access
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix="/")

    # we actually create/implement the db here
    from .models import User, Note

    with app.app_context():
        db.create_all()

    # keep track of logged in user info.

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"  # this is where we go when not logged in.
    login_manager.init_app(app)  # tells login manager what app we are using it for.

    @login_manager.user_loader
    def load_user(id):  # we do this to describe how we laod a user
        # NOTE: We get the user from the given id to load the user.
        return User.query.get(int(id))

    return app

def create_database(app):
    # we check if there exists the db, if not we create it
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app) # creates db for app. app also has the SQLAlCHEMY URI.
        print('db created!')
