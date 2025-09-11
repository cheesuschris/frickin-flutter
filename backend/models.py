from . import db
from . import current_time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from hashids import Hashids
import os, base64

hashids = Hashids("CheesyCarrotLemonBaldmeyaKleeWill1234554321", min_length=6)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String)
    password_hash = db.Column(db.String) #I'M PRETTY SURE WE DON'T NEED THIS
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.Relationship('User', backref = 'posts', lazy=True) #gives us Post.user and User.posts
    title = db.Column(db.String(50))
    recipe = db.Column(db.String(500))
    image_uri = db.Column(db.String(255))
    tags = db.Column(ARRAY(db.String))
    comments = db.Column(ARRAY(db.String))
    timestamp = db.Column(db.DateTime, default=current_time())
    likes_count = db.Column(db.Integer)

    def get_share_post_link(self):
        #change this
        return f"https://frickin-flutter/search/{hashids.encode(id)}"

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    notified_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    post = db.Relationship('Post', backref = 'notifications', lazy=True) #gives us Notification.post and Post.notifications
    notif_type = db.Column(db.String(50)) #Either liked_post, new_post, new_comment, new_follower
    message = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=current_time())
    read = db.Column(db.Boolean, default = False)

followers_association = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('profiles.id'), primary_key=True),
    db.Column('following_id', db.Integer, db.ForeignKey('profiles.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default = current_time())
)

post_likes = db.Table('post_likes',
    db.Column('profile_id', db.Integer, db.ForeignKey('profiles.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=current_time())
)

post_comments = db.Table('post_comments',
    db.Column('profile_id', db.Integer, db.ForeignKey('profiles.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=current_time())
)

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.Relationship('User', backref = 'Profile', lazy=True) #gives us Profile.user and User.profile
    bio = db.Column(db.String(300))
    username = db.Column(db.String(100))
    profile_picture_uri = db.Column(db.String(255))
    posts = db.relationship('Post',
                            primaryjoin='Profile.user_id == Post.user_id',
                            backref='author',
                            lazy=True) #gives us Profile.posts and Post.author
    notifications = db.relationship('Notification', backref='profile', lazy=True) #gives us Profile.notifications and Notification.profile
    account_created = db.Column(db.DateTime, default=current_time())
    liked_posts = db.relationship('Post', 
                                secondary=post_likes,
                                backref=db.backref('liked_by', lazy='dynamic'),
                                lazy='dynamic') #gives us Profile.liked_posts and Post.like_by
    light_mode = db.Column(db.Boolean, default=True)
    language = db.Column(db.String(50), default="English")
    #Own user comments should appear first, calculate in real time
    commented_posts = db.relationship('Post', 
                                        secondary=post_comments,
                                        backref=db.backref('commented_by', lazy='dynamic'),
                                        lazy='dynamic') #gives us Profile.commented_posts and Post.commented_by
    #Later down the road, switch followers and following to a graphDB for better mutual suggestions
    following = db.relationship('Profile', 
                                secondary = followers_association,
                                primaryjoin=id == followers_association.c.follower_id,
                                secondaryjoin=id == followers_association.c.following_id,
                                backref = 'followers',
                                lazy='dynamic'
                                )
    follower_count = db.Column(db.Integer, default=0)
    following_count = db.Column(db.Integer, default=0)
    def follow(self, profile):
        #TODO
        """Unimplemented"""
    
    def unfollow(self, profile):
        #TODO
        #SHOULD SUPPORT A DELETE METHOD, IDEMPOTENT --> ONLY DELETE IF THE FOLLOW IS FOUND
        """Unimplemented"""

    def is_following(self, profile):
        #TODO
        """Unimplemented"""

    def like_post(self, post):
        #TODO
        """Unimplemented"""

    def unlike_post(self, post):
        #TODO
        #SHOULD SUPPORT A DELETE METHOD, IDEMPOTENT --> ONLY DELETE IF THE LIKE IS FOUND
        """Unimplemented"""

    def has_liked_post(self, post):
        #TODO
        """Unimplemented"""
    
    def comment_on_post(self, post):
        #TODO
        """Unimplemented"""

    def delete_comment_on_post(self, post):
        #TODO
        #SHOULD SUPPORT A DELETE METHOD, IDEMPOTENT --> ONLY DELETE IF THE COMMENT IS FOUND
        """Unimplemented"""
    
    def has_commented_on_post(self, post):
        #TODO
        """Unimplemented"""

    def get_share_profile_link(self):
        #change this
        return f"https://frickin-flutter/profile/{hashids.encode(id)}"
   
