from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

app=Flask(__name__)
app.config['SECRET_KEY']="my secret key"
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///my_socialapp.db'

# folder configuration for image upload
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'my_social_app/static/images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# JWT configuration
app.config['JWT_SECRET_KEY'] = 'xyz'
app.config['JWT_EXPIRATION_TIME'] = 3600  # seconds
db = SQLAlchemy(app)
jwt= JWTManager(app) 


from controller.user import user_bp
from controller.follow import follow_bp
from controller.post import post_bp
from controller.post_likeAndComment import like_bp,comment_bp
from controller.feed import feed_bp

app.register_blueprint(user_bp,url_prefix='/mysocial/v1/user')
# /mysocial/v1/user/register
# /mysocial/v1/user/login
# /update_profile
app.register_blueprint(follow_bp,url_prefix='/mysocial/v1/follow')
# /mysocial/v1/follow/followuser
# /mysocial/v1/follow/unfollow
app.register_blueprint(post_bp,url_prefix='/mysocial/v1/post')
# /mysocial/v1/post/createPost
app.register_blueprint(like_bp,url_prefix='/mysocial/v1/post')
# /mysocial/v1/post/like
app.register_blueprint(comment_bp,url_prefix='/mysocial/v1/post')
# /mysocial/v1/post/commentPost
# /mysocial/v1/post/deleteComment
app.register_blueprint(feed_bp,url_prefix='/mysocial/v1/feed')
# /mysocial/v1/feed/home
# /mysocial/v1/feed/profile
# /mysocial/v1/feed/showallFollowings
# /mysocial/v1/feed/showallFollowers

with app.app_context():
    db.create_all()