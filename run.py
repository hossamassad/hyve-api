from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5433/hyve'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# User Model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.id}: {self.name}>'

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email}


# Product Model
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f'<Product {self.id}: {self.name}>'

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'price': self.price}


# UserProduct Model (Many-to-Many Relationship)
class UserProduct(db.Model):
    __tablename__ = 'user_products'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)

    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id

    def __repr__(self):
        return f'<UserProduct {self.user_id}:{self.product_id}>'

# API Endpoints for Users
@app.route('/users', methods=['GET'])
def get_all_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    users = User.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify([user.to_dict() for user in users.items]), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.filter_by(id=user_id).one()
        return jsonify(user.to_dict()), 200
    except NoResultFound:
        return jsonify({'error': 'User not found'}), 404


@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    if not name or not email:
        return jsonify({'error': 'Name and email are required'}), 400
    try:
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email already exists'}), 400


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.filter_by(id=user_id).one()
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        if name:
            user.name = name
        if email:
            user.email = email
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except NoResultFound:
        return jsonify({'error': 'User not found'}), 404


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.filter_by(id=user_id).one()
        db.session.delete(user)
        db.session.commit()
        return '', 204
    except NoResultFound:
        return jsonify({'error': 'User not found'}), 404


# API Endpoints for Products
@app.route('/products', methods=['GET'])
def get_all_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    products = Product.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify([product.to_dict() for product in products.items]), 200


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = Product.query.filter_by(id=product_id).one()
        return jsonify(product.to_dict()), 200
    except NoResultFound:
        return jsonify({'error': 'Product not found'}), 404


@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    if not name or not price:
        return jsonify({'error': 'Name and price are required'}), 400
    try:
        product = Product(name=name, price=price)
        db.session.add(product)
        db.session.commit()
        return jsonify(product.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Product already exists'}), 400


@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        product = Product.query.filter_by(id=product_id).one()
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        if name:
            product.name = name
        if price:
            product.price = price
        db.session.commit()
        return jsonify(product.to_dict()), 200
    except NoResultFound:
        return jsonify({'error': 'Product not found'}), 404


@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        product = Product.query.filter_by(id=product_id).one()
        db.session.delete(product)
        db.session.commit()
        return '', 204
    except NoResultFound:
        return jsonify({'error': 'Product not found'}), 404


# API Endpoints for User Products
@app.route('/users/<int:user_id>/products', methods=['GET'])
def get_user_products(user_id):
    try:
        user = User.query.filter_by(id=user_id).one()
        products = user.products
        return jsonify([product.to_dict() for product in products]), 200
    except NoResultFound:
        return jsonify({'error': 'User not found'}), 404


@app.route('/users/<int:user_id>/products', methods=['POST'])
def add_user_product(user_id):
    try:
        user = User.query.filter_by(id=user_id).one()
        data = request.get_json()
        product_id = data.get('product_id')
        if not product_id:
            return jsonify({'error': 'Product ID is required'}), 400
        product = Product.query.filter_by(id=product_id).one()
        user_product = UserProduct(user_id=user_id, product_id=product_id)
        db.session.add(user_product)
        db.session.commit()
        return jsonify({'message': f'Product {product.name} added to user {user.name}'}), 201
    except NoResultFound:
        return jsonify({'error': 'User or product not found'}), 404
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Product already associated with user'}), 400


@app.route('/users/int:user_id/products/int:product_id', methods=['DELETE'])
def remove_user_product(user_id, product_id):
    try:
        user = User.query.filter_by(id=user_id).one()
        product = Product.query.filter_by(id=product_id).one()
        user_product = UserProduct.query.filter_by(user_id=user_id, product_id=product_id).one()
        db.session.delete(user_product)
        db.session.commit()
        return jsonify({'message': f'Product {product.name} removed from user {user.name}'}), 204
    except NoResultFound:
        return jsonify({'error': 'User or product not found'}), 404
    
    
@app.route('/users/<int:user_id>/products', methods=['POST'])
def add_user_product_id(user_id):
    try:
        user = User.query.filter_by(id=user_id).one()
        data = request.get_json()
        product_id = data.get('product_id')
        if not product_id:
            return jsonify({'error': 'Product ID is required'}), 400
        product = Product.query.filter_by(id=product_id).one()
        user_product = UserProduct(user_id=user_id, product_id=product_id)
        db.session.add(user_product)
        db.session.commit()
        return jsonify({'message': f'Product {product.name} added to user {user.name}'}), 201
    except NoResultFound:
        return jsonify({'error': 'User or product not found'}), 404
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Product already associated with user'}), 400
    
    
if __name__ == '__main__':
    app.run()