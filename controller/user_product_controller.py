from flask import Blueprint, request, jsonify
from services.user_products import get_user_products,add_user_product,delete_user_product

api_bp = Blueprint('api', __name__)

@api_bp.route('/users/<int:user_id>/products')
def user_products(user_id):
    if request.method == 'GET':
        return jsonify(get_user_products(user_id))

    elif request.method == 'POST':
        product_id = request.json.get('product_id')
        return jsonify(add_user_product(user_id, product_id))


@api_bp.route('/users/<int:user_id>/products/<int:product_id>', methods=['DELETE'])
def user_product(user_id, product_id):
    return jsonify(delete_user_product(user_id, product_id))