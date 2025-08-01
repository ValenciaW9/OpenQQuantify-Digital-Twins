# Valencia Walker's routes.py

from flask import Blueprint, request, jsonify
from backend.models import User, Base, pwd_context
from database.database import SessionLocal, engine
from jose import jwt, JWTError
import datetime

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

SECRET_KEY = "your_super_secret_key"  # Load from .env in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

Base.metadata.create_all(bind=engine)

def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + (expires_delta if expires_delta else datetime.timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@auth_bp.route("/signup", methods=["POST"])
def signup():
    db = SessionLocal()
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = db.query(User).filter(User.email == email).first()
    if user:
        return jsonify({"error": "User already exists"}), 400

    new_user = User(email=email)
    new_user.set_password(password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"sub": email})
    return jsonify({"access_token": access_token, "token_type": "bearer"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    db = SessionLocal()
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = db.query(User).filter(User.email == email).first()
    if not user or not user.verify_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(data={"sub": email}, expires_delta=datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return jsonify({"access_token": access_token, "token_type": "bearer"}), 200
