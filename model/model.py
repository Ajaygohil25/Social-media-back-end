from app import db
from datetime import datetime

class user(db.Model):
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), nullable=False, unique=True)
    bio = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.String(6), nullable=False)
    dateofbirth = db.Column(db.Date(), nullable=False)
    contact_no = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(800), nullable=False)
    create_date = db.Column(db.DateTime)
    create_ip = db.Column(db.String(45))
    update_date = db.Column(db.DateTime)
    update_ip = db.Column(db.String(45))

    # Define relationships
    following = db.relationship('Follow', foreign_keys='Follow.follower_id', back_populates='follower', lazy=True)
    followers = db.relationship('Follow', foreign_keys='Follow.followed_id', back_populates='followed', lazy=True)

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.userid', ondelete='CASCADE'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.userid', ondelete='CASCADE'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # Define relationships
    follower = db.relationship('user', foreign_keys=[follower_id], back_populates='following')
    followed = db.relationship('user', foreign_keys=[followed_id], back_populates='followers')

class user_post(db.Model):
    post_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_owner= db.Column(db.Integer, db.ForeignKey('user.userid', ondelete='CASCADE'), nullable=False)
    post_image=db.Column(db.String(150),nullable=True)
    post_content=db.Column(db.String(100), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class post_like(db.Model):
    post_like_id = db.Column(db.Integer, primary_key=True)
    post_id= db.Column(db.Integer, db.ForeignKey('user_post.post_id', ondelete='CASCADE'), nullable=False)
    liked_by= db.Column(db.Integer, db.ForeignKey('user.userid', ondelete='CASCADE'), nullable=False)

class post_comment(db.Model):
    post_commnet_id = db.Column(db.Integer, primary_key=True)
    post_id= db.Column(db.Integer, db.ForeignKey('user_post.post_id', ondelete='CASCADE'), nullable=False)
    comment_by= db.Column(db.Integer, db.ForeignKey('user.userid', ondelete='CASCADE'), nullable=False)
    comment=db.Column(db.String(150),nullable=False)