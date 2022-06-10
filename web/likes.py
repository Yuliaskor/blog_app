from flask import request, flash, redirect, url_for, Blueprint, jsonify
from flask_login import current_user, login_required

from web import db
from web.models import Post, Like

likes = Blueprint("likes", __name__)


#dodaje polubienia, a jeśli są już dodane to usuwa
@likes.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    post_like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif post_like:
        db.session.delete(post_like)
        db.session.commit()
    else:
        post_like = Like(author=current_user.id, post_id=post_id)
        db.session.add(post_like)
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})