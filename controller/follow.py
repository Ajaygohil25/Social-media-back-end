from app import db
from model.model import Follow,user
from flask import jsonify,request, Blueprint
from flask_jwt_extended import get_jwt_identity,jwt_required

follow_bp=Blueprint('follow',__name__)
@follow_bp.route('/followuser', methods=['GET', 'POST'])
@jwt_required()
def follow_user():
    current_user_id = get_jwt_identity()
    followed_id = request.form.get('followed_user_id')
    # Validate that the following_id is a valid integer
    if not followed_id or not followed_id.isdigit():
        return jsonify({"message": "Please provide a valid user ID"}), 400
    
    if followed_id is None:
        return jsonify({"message": "Please provide enough data"}), 400

    followed_id = int(followed_id)

    # if user id is same as input id
    if followed_id == current_user_id:
        return jsonify({"message": "You can't follow yourself"}), 400

    # Check if already following
    existing_follow = Follow.query.filter_by(follower_id=current_user_id, followed_id=followed_id).first()
    if existing_follow:
        return jsonify({"message": "You are already following this user"}), 400

    #check for valid user id if user is exist or not
    existing_user= user.query.filter_by(userid=followed_id).first()
    if existing_user is None:
        return jsonify({"message": "User not exist"}), 400
    
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

    # Check if both id is same
    if following_id == current_user_id:
        return jsonify({"message": "You can't unfollow yourself"}), 400

    # Check if the user is already follow user or not
    follow_data = Follow.query.filter_by(follower_id=current_user_id, followed_id=following_id).first()
    if not follow_data:
        return jsonify({"message": "You are not following this user"}), 400
    
    follow_data.followed_id=0
    db.session.add(follow_data)
    db.session.commit()
    return jsonify({"message": "Unfollowed Successfully",})

