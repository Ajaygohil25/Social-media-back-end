from app import db,app
from model import user_post
from flask import jsonify,request, Blueprint
from flask_jwt_extended import get_jwt_identity,jwt_required
from datetime import datetime
import os
post_bp= Blueprint('post',__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}  # Allowed file types
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Logic explanation: I am creating a social media app like Twitter OR X,
#where user can upload image or only upload content 

# for create post
@post_bp.route('/createPost', methods=['POST'])
@jwt_required()
def createPost():
    try:
        current_userid = get_jwt_identity()
        #If there is no Image post only content
        if request.form!='image_file':
            content = request.form.get('content')
            image_file = None
        # If there is post image    
        else:
            content = request.form.get('content')
            image_file = request.files['image_file']
            if image_file.filename == '':
                image_file=None
            # post image logic 
            if image_file and allowed_file(image_file.filename):
                filename = image_file.filename
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(image_path)
            else:
                return jsonify({"message": "Invalid file format. Only PNG, JPG, JPEG allowed."}), 400
        #save to database
        new_post = user_post(
            post_owner=current_userid, post_content=content,
            post_image=filename if image_file else 'default.jpg', timestamp=datetime.now())        
        db.session.add(new_post)
        db.session.commit()
        return jsonify({"message": "Post created successfully"}),200
    except Exception as e:
            db.session.rollback()
            return str(e), 500

# User can only update content of the post, but cannot update image as instagram and twitter
@post_bp.route('/updatePost', methods=['POST'])
@jwt_required()
def updatePost():
    post_id= request.form.get('post_id')
    updated_content = request.form.get('content')
    try:
        if post_id is not None and updated_content is not None:
            post_data= user_post.query.filter_by(post_id=post_id).first()
            post_data.post_content=updated_content
            db.session.add(post_data)
            db.session.commit()
            return jsonify({"message": "Post updated successfully"}),200
        else:
            return jsonify({"message": "Please Give enough data "}),400
    except Exception as e:
        db.session.rollback()
        return str(e), 500

#User can delete Entire post 
@post_bp.route('/deletePost', methods=['POST'])
def deletePost():
    post_id= request.form.get('post_id')
    try:
        if post_id is not None:
            post_data= user_post.query.filter_by(post_id=post_id).first()
            db.session.delete(post_data)
            db.session.commit()
            return jsonify({"message": "Post Deleted successfully"}),200
        else:
            return jsonify({"message": "Please Give enough data "}),400
    except Exception as e:
        db.session.rollback()
        return str(e), 500


    

             