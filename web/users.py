from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from web import db
from web.models import UserFriend, User

users = Blueprint("users", __name__)

@users.route("/users")
@login_required
def users_list():
    user_list = User.query.all()
    return render_template("users.html", users=user_list)
@users.route("/add-friends/<friend_id>")
@login_required
def add_friend(friend_id):

    friend = User.query.filter_by(id=friend_id).first()
    if not friend:
        flash('User does not exist.', category='error')
    elif current_user.id == int(friend_id):
        flash('You can\'t by friend of yourself.', category='error')
    elif any(friendship.friend == int(friend_id) for friendship in current_user.friends):
        flash('It\'s already your friend', category='error')
    else:
        user_friend = UserFriend(user=current_user.id, friend=friend_id)
        db.session.add(user_friend)
        db.session.commit()
        flash('Friend add!', category='success')
        return redirect(url_for('posts.posts_user', username=friend.username))

    return redirect(url_for('posts.posts_user', username=friend.username))


@users.route("/remove-friends/<friend_id>")
@login_required
def remove_friend(friend_id):

    friend = User.query.filter_by(id=friend_id).first()
    if not friend:
        flash('User does not exist.', category='error')
    elif current_user.id == int(friend_id):
        flash('You can\'t remove yourself.', category='error')
    else:
        user_friend = UserFriend.query.filter_by(user=current_user.id, friend=friend_id).first()
        db.session.delete(user_friend)
        db.session.commit()
        flash('Friend removed!', category='success')
        return redirect(url_for('posts.posts_user', username=friend.username))

    return redirect(url_for('posts.posts_user', username=friend.username))

