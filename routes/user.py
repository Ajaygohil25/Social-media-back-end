from flask import Blueprint, jsonify, request
from datetime import datetime,timezone
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app import db
from model import user
from common.validators import Validator
from flask_bcrypt import Bcrypt

user_bp = Blueprint('user', __name__)
bcrypt = Bcrypt()
validator = Validator()

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = validator.validate_registration_data(data)
    if errors:
        return jsonify({"errors": errors}), 400

    username = data['username']
    bio = data.get('bio')
    gender = data.get('gender')
    dateinput = data.get('dateofbirth')
    contact = data['contact']
    email = data['email']
    password = data['password']

    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        dateofbirth = datetime.strptime(dateinput, '%Y-%m-%d').date()
        new_user = user(username=username, bio=bio, gender=gender, dateofbirth=dateofbirth, contact_no=contact, email=email, password=hashed_password, create_date=datetime.now(timezone.utc),create_ip=request.remote_addr, update_date = datetime.now(timezone.utc),update_ip = request.remote_addr)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 200
    except ValueError as e:
        return str(e), 400
    except Exception as e:
        db.session.rollback()
        return str(e), 500

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    errors = validator.validate_login_data(data)
    if errors:
        return jsonify({"errors": errors}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Please enter Username and Password"}), 400

    userdata = user.query.filter_by(username=username).first()
    if userdata and bcrypt.check_password_hash(userdata.password, password):
        access_token = create_access_token(identity=userdata.userid)
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@user_bp.route('/update_profile', methods=['POST'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    data = request.json
    errors = validator.validate_data(data)
    if errors:
        return jsonify({"errors": errors}), 400

    userdata = user.query.filter_by(userid=current_user_id).first()
    if not userdata:
        return jsonify({"message": "User not found."}), 404

    username = data.get('username')
    bio = data.get('bio')
    gender = data.get('gender')
    dateofbirth_str = data.get('dateofbirth')
    contact_no = data.get('contact_no')
    email = data.get('email')
    password = data.get('password')

    if username:
        if user.query.filter_by(username=username).first() and username != userdata.username:
            return jsonify({"message": "Username already exists."}), 400
        userdata.username = username
    if bio:
        userdata.bio = bio
    if gender:
        userdata.gender = gender
    if dateofbirth_str:
        try:
            dateofbirth = datetime.strptime(dateofbirth_str, '%Y-%m-%d').date()
            userdata.dateofbirth = dateofbirth
        except ValueError:
            return jsonify({"message": "Invalid date format. Use YYYY-MM-DD."}), 400
    if contact_no:
        userdata.contact_no = contact_no
    if email:
        userdata.email = email
    if password:
        userdata.password = password
    
    userdata.update_date = datetime.now(timezone.utc)
    userdata.update_ip = request.remote_addr

    try:
        db.session.add(userdata)
        db.session.commit()
        return jsonify({"message": "Profile updated successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
