from app import db
from model import Follow,user
from flask import jsonify,request, Blueprint
from flask_jwt_extended import get_jwt_identity,jwt_required

follow_bp=Blueprint('follow',__name__)
@follow_bp.route('/followuser', methods=['GET', 'POST'])
@jwt_required()
def follow_user():
    current_user_id = get_jwt_identity()
    followed_id = request.form.get('followed_user_id')

    if followed_id is None:
        return jsonify({"message": "Please provide enough data"}), 400

    followed_id = int(followed_id)

    # Check if the user is trying to follow themselves
    if followed_id == current_user_id:
        return jsonify({"message": "You can't follow yourself"}), 400

    # Check if already following
    existing_follow = Follow.query.filter_by(follower_id=current_user_id, followed_id=followed_id).first()
    if existing_follow:
        return jsonify({"message": "You are already following this user"}), 400

    # Add the follow relationship
    new_follow = Follow(follower_id=current_user_id, followed_id=followed_id)
    db.session.add(new_follow)
    db.session.commit()

    return jsonify({"message": "You are now following the user"}), 200

@follow_bp.route('/unfollow', methods=['POSt'])
@jwt_required()
def unfollow():
    current_user_id= get_jwt_identity()
    following_id =request.form.get('following_user_id')
    # Validate that the following_id is a valid integer
    if not following_id or not following_id.isdigit():
        return jsonify({"message": "Please provide a valid user ID"}), 400
    
    following_id = int(following_id)

    # Check if the user is trying to unfollow themselves
    if following_id == current_user_id:
        return jsonify({"message": "You can't unfollow yourself"}), 400

    # Check if the user is actually following the target user
    follow_data = Follow.query.filter_by(follower_id=current_user_id, followed_id=following_id).first()
    if not follow_data:
        return jsonify({"message": "You are not following this user"}), 400
    
    follow_data.followed_id=0
    db.session.add(follow_data)
    db.session.commit()
    return jsonify({"message": "Unfollowed Successfully",})

@follow_bp.route('/showallFollowings', methods=['GET'])
@jwt_required()
def showallFollowings():
    current_user_id= get_jwt_identity()
    followuser_list = Follow.query.filter_by(follower_id=current_user_id).filter(Follow.followed_id > 0).all()
    following=[]
    for follow in followuser_list:
        follow_user = user.query.get(follow.followed_id)
        if follow_user is not None:
            following.append({'user name ': follow_user.username})
    return jsonify(following)        

@follow_bp.route('/showallFollowers', methods=['GET'])
@jwt_required()
def showallFollowers():
    current_user_id= get_jwt_identity()
    follower_list = Follow.query.filter_by(followed_id=current_user_id).all()
    followers=[]
    for follow in follower_list:
        follower_user = user.query.get(follow.followed_id)
        if follower_user is not None:
            followers.append({'username ': follower_user.user})
    return jsonify(followers)
