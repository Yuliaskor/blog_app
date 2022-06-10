from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "blog.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "DFEKLJFMEIJFIJXW65443P"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .auth import auth
    from .comments import comments
    from .likes import likes
    from .posts import posts
    from .users import users
    from .home import home

    app.register_blueprint(home, url_prefix="/")
    app.register_blueprint(users, url_prefix="/")
    app.register_blueprint(comments, url_prefix="/")
    app.register_blueprint(likes, url_prefix="/")
    app.register_blueprint(posts, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    create_database(app)
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


def create_database(app):
    if not path.exists("website/"+ DB_NAME):
        db.create_all(app=app)