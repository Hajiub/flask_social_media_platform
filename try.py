 def is_visible_to_user(self, user):
        # Check if the user is the owner of the post
        if user.id == self.user_id:
            return True

        # Check if the user is friends with the owner of the post
        friends = FriendList.query.filter_by(user_id=user.id).all()
        friend_ids = [friend.friend_id for friend in friends]
        
        return self.user_id in friend_ids

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