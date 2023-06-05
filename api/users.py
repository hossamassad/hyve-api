from flask import Blueprint, request, jsonify
from database import db
from model.user import Users
from utils.validation import validate_user_data
from utils.pagination import paginate

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    users = Users.query.order_by(Users.id).all()
    paginated_users = paginate(users, page, per_page)
    return jsonify([user.to_dict() for user in paginated_users])

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user.to_dict())

@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    error = validate_user_data(data)
    if error:
        return jsonify({'message': error}), 400
    new_user = Users(name=data['name'], email=data['email'], role=data['role'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    data = request.get_json()
    error = validate_user_data(data)
    if error:
        return jsonify({'message': error}), 400
    user.name = data['name']
    user.email = data['email']
    user.role = data['role']
    user.password = data['password']
    db.session.commit()
    return jsonify(user.to_dict())

@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})