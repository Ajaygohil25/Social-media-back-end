from app import db
from model.model import post_like,user_post,post_comment,Follow,user
from flask import jsonify,request, Blueprint
from flask_jwt_extended import get_jwt_identity,jwt_required
from datetime import datetime
feed_bp= Blueprint('feed',__name__)
@feed_bp.route('/home',methods=['GET'])
@jwt_required()
def home():
    current_user = get_jwt_identity()
    list_of_followings = Follow.query.filter_by(follower_id=current_user).filter(Follow.followed_id > 0).all()
    user_feed = []
    if list_of_followings:
        for follow in list_of_followings:
            # Fetch posts for each followed user
            following_user_posts = user_post.query.filter_by(post_owner=follow.followed_id).all()

            for post in following_user_posts:
                post_data = {
                    "user_id": post.post_owner,
                    "content": post.post_content,
                    "timestamp": post.timestamp
                }
                if post.post_image:
                    post_data["image"] = post.post_image
                
                user_feed.append(post_data)
        if user_feed:
            return jsonify(user_feed)
        else:
            return jsonify({"message": "You're following users have not uploaded any content"}), 400
    else:
        return jsonify({"message": "You're not following any user"}), 400


@feed_bp.route('/profile',methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    userdata = user.query.get(current_user)
    profile={
        "username": userdata.username,
        "bio": userdata.bio,
        "Gender": userdata.gender,
        "Date of Birth": userdata.dateofbirth,
        "email": userdata.email
    }
    return jsonify(profile)
# show all following by current user
@feed_bp.route('/showallFollowings', methods=['GET'])
@jwt_required()
def showallFollowings():
    current_user_id= get_jwt_identity()
    followuser_list = Follow.query.filter_by(follower_id=current_user_id).filter(Follow.followed_id > 0).all()
    following=[]
    if followuser_list is not None:
        for follow in followuser_list:
            follow_user = user.query.get(follow.followed_id)
            if follow_user is not None:
                following.append({'user name ': follow_user.username})
        return jsonify(following)     
    else:
        return jsonify({"message": "You're not following any user"}), 400  

#show all followers
@feed_bp.route('/showallFollowers', methods=['GET'])
@jwt_required()
def showallFollowers():
    current_user_id= get_jwt_identity()
    follower_list = Follow.query.filter_by(followed_id=current_user_id).all()
    followers=[]
    if follower_user is not None:
        for follow in follower_list:
            follower_user = user.query.get(follow.follower_id)
            if follower_user is not None:
                followers.append({'username ': follower_user.username})
        return jsonify(followers)
    else:
        return jsonify({"message": "You're not followed by any user"}), 400



