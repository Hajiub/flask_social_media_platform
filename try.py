

from flask import render_template
from flask_login import current_user

@app.route('/posts')
def posts():
    user = current_user  # Assuming you are using Flask-Login for authentication
    
    # Retrieve all posts
    all_posts = Post.query.all()
    
    # Filter out the posts that are not visible to the current user
    visible_posts = [post for post in all_posts if post.is_visible_to_user(user)]
    
    return render_template('posts.html', posts=visible_posts)
