from flask import jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
from datetime import datetime, timedelta
from app import app, db
from model.user import User


def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return user

def generate_token(payload):
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token.decode('utf-8')

def decode_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None

def login_required(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token:
            payload = decode_token(token)
            if payload:
                user_id = payload.get('user_id')
                user = User.query.get(user_id)
                if user:
                    return func(user, *args, **kwargs)
        return jsonify({'error': 'Unauthorized access'}), 401
    return wrapper

def admin_required(func):
    def wrapper(user, *args, **kwargs):
        if user.role == 'admin':
            return func(user, *args, **kwargs)
        else:
            return jsonify({'error': 'Admin access required'}), 403
    return wrapper

def hash_password(password):
    return generate_password_hash(password)