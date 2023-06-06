from flask import Blueprint, request, jsonify
from services.users import get_all_users, get_user, add_user, update_user, delete_user

user_bp = Blueprint('api', __name__)

@user_bp.route('/users')
@user_bp.route('/users/<int:user_id>')
def users(user_id=None):
    if request.method == 'GET':
        if user_id:
            return jsonify(get_user(user_id))
        else:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            return jsonify(get_all_users(page=page, per_page=per_page))

    elif request.method == 'POST':
        name = request.json.get('name')
        email = request.json.get('email')
        return jsonify(add_user(name, email))

    elif request.method == 'PUT':
        name = request.json.get('name')
        email = request.json.get('email')
        return jsonify(update_user(user_id, name, email))

    elif request.method == 'DELETE':
        return jsonify(delete_user(user_id))
