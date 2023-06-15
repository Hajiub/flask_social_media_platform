from flask import render_template, request
from flask_login import current_user, login_required
from app.models import Post, Like, Comment,User
from sqlalchemy.orm import joinedload
from app import db
from sqlalchemy import func
import base64
from . import main




@main.route('/')
@login_required
def home():
    user = current_user  # Assuming you are using Flask-Login for authentication
    
    # Retrieve all posts
    all_posts = Post.query.all()
    
    # Filter out the posts that are not visible to the current user
    visible_posts = [post for post in all_posts if post.is_visible_to_user(user)]
    for post in visible_posts:
        post.likes_count = db.session.query(func.count(Like.id)).filter_by(post_id=post.id).scalar()
        post.comments_count = db.session.query(func.count(Comment.id)).filter_by(post_id=post.id).scalar()    
    return render_template('main/home_view.html', posts_list=visible_posts)


