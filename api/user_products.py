from flask import Blueprint, request, jsonify
from database import db
from model.user import Users
from model.product import Products
from model.user_product import UserProducts
from utils.validation import validate_user_product_data

user_products_bp = Blueprint('user_products', __name__, url_prefix='/user-products')

@user_products_bp.route('/', methods=['GET'])
def get_user_products():
    user_id = request.args.get('user_id', type=int)
    product_id = request.args.get('product_id', type=int)

    if user_id:
        user = Users.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        user_products = UserProducts.query.filter_by(user_id=user_id).all()
        return jsonify([up.to_dict() for up in user_products])

    elif product_id:
        product = Products.query.get(product_id)
        if not product:
            return jsonify({'message': 'Product not found'}), 404
        user_products = UserProducts.query.filter_by(product_id=product_id).all()
        return jsonify([up.to_dict() for up in user_products])

    else:
        return jsonify({'message': 'Please provide either user_id or product_id'}), 400

@user_products_bp.route('/', methods=['POST'])
def create_user_product():
    data = request.get_json()
    error = validate_user_product_data(data)
    if error:
        return jsonify({'message': error}), 400

    user = Users.query.get(data['user_id'])
    if not user:
        return jsonify({'message': 'User not found'}), 404

    product = Products.query.get(data['product_id'])
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    user_product = UserProducts(user_id=user.id, product_id=product.id)
    db.session.add(user_product)
    db.session.commit()

    return jsonify(user_product.to_dict()), 201

@user_products_bp.route('/<int:user_id>/<int:product_id>', methods=['DELETE'])
def delete_user_product(user_id, product_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    product = Products.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    user_product = UserProducts.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not user_product:
        return jsonify({'message': 'UserProduct not found'}), 404

    db.session.delete(user_product)
    db.session.commit()

    return jsonify({'message': 'UserProduct deleted'})