from datetime import datetime
from . import db
from . import current_time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(50))
    recipe = db.Column(db.String(500))
    image_uri = db.Column(db.String(255))
    post_comments = db.Column(ARRAY(db.string))
    timestamp = db.Column(db.DateTime, default=current_time())
    post_likes_count = db.Column(db.Integer)
    #Sharing via a link should be calculated in real time based on post id

class Notification(db.Mode):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=current_time())

#Going to be null until user updates it in settings
class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bio = db.Column(db.String(300))
    username = db.Column(db.String(100))
    profile_picture_uri = db.Column(db.String(255))
    posts = db.relationship('Post', backref='author', lazy=True)
    notifications = db.relationship('Notification', backref='notified_user', lazy=True)
    account_created = db.Column(db.DateTime, default=current_time())
    liked_posts = db.relationship('Post', backref = 'liked_by', lazy=True)
    #Own user comments should appear first, calculate in real time
    commented_posts = db.relationship('Post', backref = 'commented_by', lazy=True)

    #Later down the road, switch followers and following to a graphDB for better mutual suggestions
    followers = db.Column(ARRAY(db.Integer))
    following = db.Column(ARRAY(db.Integer))


