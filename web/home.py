from flask import Blueprint, render_template
from flask_login import login_required, current_user

from web.models import Post

home = Blueprint("home", __name__)


@home.route("/")
@home.route("/home")
@login_required
def home_():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

