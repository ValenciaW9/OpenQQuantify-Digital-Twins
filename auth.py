#auth.py -Valencia Walker's

from flask import Blueprint, request, jsonify
from database.database import SessionLocal, User, pwd_context
import jwt
import os
from datetime import datetime, timedelta

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

SECRET_KEY = os.getenv("JWT_SECRET", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    db = SessionLocal()
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    hashed_password = pwd_context.hash(password)
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return jsonify({"message": "User created successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if not user or not user.verify_password(password):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token({"sub": username})
    return jsonify({"access_token": access_token, "token_type": "bearer"})