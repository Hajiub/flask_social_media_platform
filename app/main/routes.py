from flask import render_template, request
from flask_login import current_user, login_required
from app.models import Post, Like, Comment,User
from sqlalchemy.orm import joinedload
from app import db
from sqlalchemy import func
import base64
from . import main



@main.route('/')
def home():
    posts = Post.query.options(joinedload(Post.user)).order_by(Post.created_at).all()
    for post in posts:
        post.likes_count = db.session.query(func.count(Like.id)).filter_by(post_id=post.id).scalar()
        post.comments_count = db.session.query(func.count(Comment.id)).filter_by(post_id=post.id).scalar()
    return render_template("main/home_view.html",posts_list=posts)