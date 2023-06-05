from flask import Blueprint, request, jsonify
from database import db
from model.product import Products
from utils.validation import validate_product_data
from utils.pagination import paginate

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    products = Products.query.order_by(Products.id).all()
    paginated_products = paginate(products, page, per_page)
    return jsonify([product.to_dict() for product in paginated_products])

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Products.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    return jsonify(product.to_dict())

@products_bp.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    error = validate_product_data(data)
    if error:
        return jsonify({'message': error}), 400
    new_product = Products(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Products.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    data = request.get_json()
    error = validate_product_data(data)
    if error:
        return jsonify({'message': error}), 400
    product.name = data['name']
    product.price = data['price']
    db.session.commit()
    return jsonify(product.to_dict())

@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Products.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'})