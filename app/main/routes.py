from flask import render_template, request, jsonify
from flask_login import current_user, login_required
from app.models import Post, Like, Comment,User
from sqlalchemy.orm import joinedload
from app import db
from sqlalchemy import func
import base64
from . import main


from sqlalchemy import desc

@main.route('/')
@login_required
def home():
    user = current_user  
    all_posts = Post.query.order_by(desc(Post.created_at)).all()
    visible_posts = [post for post in all_posts if post.is_visible_to_user(user)]
    # visible_posts = visible_posts[:10]
    
    for post in visible_posts:
        post.likes_count = db.session.query(func.count(Like.id)).filter_by(post_id=post.id).scalar()
        post.comments_count = db.session.query(func.count(Comment.id)).filter_by(post_id=post.id).scalar()
        
    return render_template('main/home_view.html', posts_list=visible_posts)



