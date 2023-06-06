from flask import Blueprint, request, jsonify
from services.products import get_all_products ,get_product,add_product,update_product,delete_product

product_bp = Blueprint('api', __name__)

@product_bp.route('/products')
@product_bp.route('/products/<int:product_id>')
def products(product_id=None):
    if request.method == 'GET':
        if product_id:
            return jsonify(get_product(product_id))
        else:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            return jsonify(get_all_products(page=page, per_page=per_page))

    elif request.method == 'POST':
        name = request.json.get('name')
        price = request.json.get('price')
        return jsonify(add_product(name, price))

    elif request.method == 'PUT':
        name = request.json.get('name')
        price = request.json.get('price')
        return jsonify(update_product(product_id, name, price))

    elif request.method == 'DELETE':
        return jsonify(delete_product(product_id))

