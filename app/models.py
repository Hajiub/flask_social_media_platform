from datetime import datetime
from flask_login import UserMixin
from app import db
from flask import url_for


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    profile  = db.relationship('Profile', backref='user', cascade='all, delete-orphan')
    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='user', cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='user', cascade='all, delete-orphan')
    friends = db.relationship(
        'User',
        secondary='friend_list',
        primaryjoin='User.id == FriendList.user_id',
        secondaryjoin='User.id == FriendList.friend_id',
        backref='friend_of'
    )
    friends_request = db.relationship(
        'User',
        secondary='friend_request',
        primaryjoin='User.id == FriendRequest.user_id',
        secondaryjoin='User.id == FriendRequest.friend_id',
        backref='requested_by'
    )
    def serialize(self):
        return {
            'username': self.username,
            'url': url_for("profiles.user_profile", user_id=self.id)
        }

    def __repr__(self):
        return f"<User {self.username} ({self.email})>"

# A user can have one profile only
class Profile(db.Model):
    __tablename__ = "user_profile"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    birthday = db.Column(db.Date)
    country  = db.Column(db.String(100))
    profile_pic = db.Column(db.String(255))
    bio = db.Column(db.String(500))
    intrested_at = db.Column(db.String(500))
    gender     = db.Column(db.String(10))
    interest = db.Column(db.JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False, unique=True)
    
class Post(db.Model):
    __tablename__ = 'post'

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content    = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_img   = db.Column(db.String(255))
    tags       = db.Column(db.JSON)
    likes      = db.relationship('Like', backref='post', cascade='all, delete-orphan')
    comments   = db.relationship('Comment', backref='post', cascade='all, delete-orphan')

    # Todo Remove this function form here !!
    def is_visible_to_user(self, user):
        # Check if the user is the owner of the post
        if user.id == self.user_id:
            return True

        # Check if the user is friends with the owner of the post
        friends = FriendList.query.filter_by(user_id=user.id).all()
        friend_ids = [friend.friend_id for friend in friends]

        return self.user_id in friend_ids

    def __repr__(self):
        return f"<Post {self.id} -- {self.content}>"


class Like(db.Model):
    __tablename__ = 'like'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Like {self.id}>"


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Comment {self.id}>"


class FriendList(db.Model):
    __tablename__ = 'friend_list'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<FriendList {self.user_id} -- {self.friend_id}>"


class Notification(db.Model):
    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_seen = db.Column(db.Boolean, default=False, nullable=False)
    user = db.relationship('User', backref='notifications')

    def __repr__(self):
        return f"<Notification {self.id} -- {self.message}>"


class FriendRequest(db.Model):
    __tablename__ = 'friend_request'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, unique=True)
    sented_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<FriendRequest {self.user_id} -- {self.friend_id}>"


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Message {self.id} -- {self.content}>"


