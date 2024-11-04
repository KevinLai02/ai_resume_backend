from flask import request, jsonify
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import Session
from db.database import get_db
from db.User.User_model import get_user_by_email, create_user
from utils.account import generate_jwt


def signUp():
    db: Session = next(get_db())
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    user = get_user_by_email(db, user_email=email)
    if user: 
        return jsonify({"message": "Email already exist"}), 403

    bcrypt = Bcrypt()
    hashPassword = bcrypt.generate_password_hash(password=password)
    encodePassword = hashPassword.decode("utf-8", "ignore")
    new_user = create_user(db, name=name, email=email, password=encodePassword)
    new_user_data = {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
    }
    token = generate_jwt(new_user.id)

    return jsonify({"message": "SignUp successful", "data": new_user_data, "token": token}), 200

def login():
    db: Session = next(get_db())
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    user = get_user_by_email(db, user_email=email)
    if not user: 
        return jsonify({"message": "User is not exist"}), 403

    hashPassword = user.password
    bcrypt = Bcrypt()
    isPasswordCorrect = bcrypt.check_password_hash(hashPassword, password)

    user_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }
    
    if isPasswordCorrect:
        token = generate_jwt(user.id)
        return jsonify({"message": "Login successful", "token": token, "data": user_data}), 200
    else:
        return jsonify({"message": "Email or Password is not correct"}), 403