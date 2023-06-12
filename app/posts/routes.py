from . import post
from flask import render_template, redirect, url_for, request, current_app, flash, session, abort
from app.models import Post, Like, Comment, User
from app.forms import CreatePostForm, CreateCommentForm, UpdatePostForm
from flask_login import current_user, login_required
import os 
from werkzeug.utils import secure_filename
from .utils import allowed_file, PostUpdater
from app import db, csrf
import uuid
from sqlalchemy.orm import joinedload

@post.route('/post', methods=['POST', 'GET'])
@login_required
@csrf.exempt
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        content = form.content.data
        image = form.data.get('image')
        
        if image and allowed_file(image.filename):
            uuid1_value = uuid.uuid1()
            img_name = str(uuid1_value) + secure_filename(image.filename) 
            try:
                path = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.email, "post_images", img_name)
                post = Post(user_id=current_user.id, content=content, post_img=os.path.join('post_images', img_name))
                db.session.add(post)
                db.session.commit()
                image.save(path)
            except Exception as e:
                flash('Something went wrong. Please try again! Error: ' + str(e))
                return redirect(url_for('post.create_post'))
                
            flash('Your post has been added successfully!')
            return redirect(url_for('main.home'))

        post = Post(user_id=current_user.id, content=content)
        db.session.add(post)
        db.session.commit()

        flash('Your post has been added successfully!')
        return redirect(url_for('main.home'))

    return render_template('post/create_post.html', form=form)
@post.route('/detail/<int:post_id>')
@login_required
def detail_post_view(post_id):
    form = CreateCommentForm()
    post = Post.query.get_or_404(post_id)
    if post:
        post = (
            Post.query
            .options(joinedload(Post.user))
            .filter(Post.id == post_id)
            .first()
        )
        comments = (
            Comment.query
            .join(User)
            .filter(Comment.post_id == post_id)
            .all()
        )
        likes = (
            Like.query
            .join(User)
            .filter(Like.post_id == post_id)
            .all()
        )
        return render_template('post/post_detail.html', post=post, comments=comments, likes=likes, form=form)
    
@post.route('/comment/<int:post_id>', methods=['POST'])
@csrf.exempt
@login_required
def comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post:
        content = request.form.get("content")
        comment = Comment(user_id=current_user.id, post_id=post.id, content=content)
        try:
            db.session.add(comment)
            db.session.commit()
        except Exception as e:
            flash('Error {0}'.format(str(e)))
            return redirect(url_for('post.detail_post_view', post_id=post.id))
        
        return redirect(url_for('post.detail_post_view', post_id=post.id))
    
@post.route('/like/<int:post_id>')
@login_required
def like_post_view(post_id):
    post =  Post.query.get_or_404(post_id)
    if post:
        if like := Like.query.filter_by(user_id=current_user.id, post_id=post.id).first():
            db.session.delete(like)
            db.session.commit()
            return redirect(url_for('main.home'))
        like = Like(user_id=current_user.id, post_id=post.id)
        db.session.add(like)
        db.session.commit()
        return redirect(url_for('main.home'))
        
@post.route('/update/<int:post_id>', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = UpdatePostForm()

    if form.validate_on_submit():
        if session.get('_csrf_token') != request.form.get('_csrf_token'):
            return abort(400, 'Invalid CSRF Token')

        try:
            updater = PostUpdater(current_app, current_user)            
            updater.update_post_fields(post, form)
            db.session.commit()
            return redirect(url_for('main.home'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the post.', 'error')

    return render_template('post/update_post.html', form=form, post=post)



@post.route('/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post:
        if post.post_img:
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.email, post.post_img)
            os.remove(image_path)
        try:
            db.session.delete(post)
            db.session.commit()

            flash('Your post has been removed successfully!')
            return redirect(url_for('main.home'))
        except:
            flash('Something went wrong please try again')
            return redirect(url_for('main.home'))