from app import  db
from model import post_like,user_post,post_comment
from flask import jsonify,request, Blueprint
from flask_jwt_extended import get_jwt_identity,jwt_required

#Functionality of post like
like_bp= Blueprint('like',__name__)
@like_bp.route('/likePost',methods=['POST'])
@jwt_required()
def likePost():
    current_user = get_jwt_identity()
    post_id = request.form.get('post_id')
    # Check if post exists
    post = user_post.query.filter_by(id=post_id).first()
    try:
        if post is not None:
            # Check if the post is already liked by the current user
            liked_post = post_like.query.filter_by(post_id=post_id, liked_by=current_user).first()
            
            if liked_post is None:
                # Post is not liked yet, so like it
                likepost = post_like(post_id=post_id, liked_by=current_user)
                db.session.add(likepost)
                db.session.commit()
                return jsonify({"message": "Post liked successfully"}), 200
            else:
                # Post is already liked, so unlike it
                db.session.delete(liked_post)
                db.session.commit()
                return jsonify({"message": "Post unliked successfully"}), 200
        else:
            return jsonify({"message": "Post not found"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Functionality of comment
comment_bp= Blueprint('comment',__name__)
@comment_bp.route('/commentPost',methods=['POST'])
@jwt_required()
def commentPost():
    current_user= get_jwt_identity()
    post_id=request.form.get('post_id')
    comment=request.form.get('comment')
    # check if post is existing or not
    post= user_post.query.filter_by(post_id=post_id).first()
    try:
        if post_id is not None and post.post_id is not None:
            comment_post=post_comment(post_id=post_id, comment_by=current_user,comment=comment)
            db.session.add(comment_post)
            db.session.commit()
            return jsonify({"message": "Comment added successfully"}),200
        else:
            return jsonify({"message": "Please Give correct data "}),400
    except Exception as e:
        db.session.rollback()
        return str(e), 500    
# delete comment 
@comment_bp.route('/deleteComment', methods=['POST'])
@jwt_required()
def deleteComment():
    comment_id=request.form.get('comment_id')
    comment = post_comment.query.filter_by(post_commnet_id=comment_id).first()
    try:
        if comment is not None and comment_id is not None:
            db.session.delete(comment)
            db.session.commit()
            return jsonify({"message": "Comment deleted successfully"}),200
        else:
            return jsonify({"message": "Please Give correct data "}),400
    except Exception as e:  
         db.session.rollback()
         return str(e), 500   


    
