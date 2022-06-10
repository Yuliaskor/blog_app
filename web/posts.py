from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from web import db
from web.models import Post, User

posts = Blueprint("posts", __name__)


#class dla zarządzania postami
@posts.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('home.home_'))

    return render_template('create_post.html', user=current_user)


@posts.route("/delete-post/<id>")
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('home.home_'))


@posts.route("/posts/<username>")
@login_required
def posts_user(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('home.home_'))

    posts_list = Post.query.filter_by(author=user.id).all()

    return render_template("posts.html", posts=posts_list, username=username, id=user.id, is_friend=
                           any(friendship.friend == user.id for friendship in current_user.friends))


@posts.route("/posts")
@login_required
def all_posts():
    posts_list = Post.query.all()
    return render_template("posts.html", posts=posts_list)


@posts.route("/friends/posts")
@login_required
def posts_friend():
    f_posts = Post.query.filter(Post.author.in_([friendship.friend for friendship in current_user.friends])).all()
    return render_template("posts.html", posts=f_posts, title="My friends posts")
