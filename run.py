from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)

# Configure database settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hyve.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.email = email

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Define Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, body, user_id):
        self.title = title
        self.body = body
        self.user_id = user_id

# Define User schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

# Define Post schema
class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post

# Create user endpoint
@app.route('/api/users', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    user = User(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token})

# Login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token})

# Get user profile endpoint
@app.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_profile(user_id):
    if user_id != get_jwt_identity():
        return jsonify({'error': 'Unauthorized'}), 401
    user = User.query.get(user_id)
    user_schema = UserSchema()
    return user_schema.jsonify(user)

# Update user profile endpoint
@app.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user_profile(user_id):
    if user_id != get_jwt_identity():
        return jsonify({'error': 'Unauthorized'}), 401
    user = User.query.get(user_id)
    user.username = request.json.get('username', user.username)
    user.email = request.json.get('email', user.email)
    db.session.commit()
    user_schema = UserSchema()
    return user_schema.jsonify(user)

# Delete user account endpoint
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user_account(user_id):
    if user_id != get_jwt_identity():
        return jsonify({'error': 'Unauthorized'}), 401
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User account deleted'})

# Get all posts endpoint
@app.route('/api/posts', methods=['GET'])
def get_all_posts():
    posts = Post.query.all()
    post_schema = PostSchema(many=True)
    return post_schema.jsonify(posts)

# Get single post endpoint
@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_single_post(post_id):
    post = Post.query.get(post_id)
    post_schema = PostSchema()
    return post_schema.jsonify(post)

# Create post endpoint
@app.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():
    title = request.json['title']
    body = request.json['body']
    user_id = get_jwt_identity()
    post = Post(title=title, body=body, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    post_schema = PostSchema()
    return post_schema.jsonify(post)

# Update post endpoint
@app.route('/api/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    if post.user_id != get_jwt_identity():
        return jsonify({'error': 'Unauthorized'}), 401
    post.title = request.json.get('title', post.title)
    post.body = request.json.get('body', post.body)
    db.session.commit()
    post_schema = PostSchema()
    return post_schema.jsonify(post)

# Delete post endpoint
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    if post.user_id != get_jwt_identity():
        return jsonify({'error': 'Unauthorized'}), 401
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted'})
# Retrieve all users endpoint
@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_all_users():
    if not get_jwt_identity():
        return jsonify({'error': 'Unauthorized'}), 401
    users = User.query.all()
    user_schema = UserSchema(many=True)
    return user_schema.jsonify(users)

# Retrieve a specific user by ID endpoint
@app.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    if user_id != get_jwt_identity():
        return jsonify({'error': 'Unauthorized'}), 401
    user = User.query.get(user_id)
    user_schema = UserSchema()
    return user_schema.jsonify(user)

# Create a new user endpoint
@app.route('/api/users', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    user = User(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token})

# Update an existing user endpoint
@app.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    if user_id != get_jwt_identity():
        return jsonify({'error': 'Unauthorized'}), 401
    user = User.query.get(user_id)
    user.username = request.json.get('username', user.username)
    user.email = request.json.get('email', user.email)
    db.session.commit()
    user_schema = UserSchema()
    return user_schema.jsonify(user)

# Delete a user endpoint
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    if user_id != get_jwt_identity():
        return jsonify({'error': 'Unauthorized'}), 401
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

# Retrieve all products endpoint
@app.route('/api/products', methods=['GET'])
def get_all_products():
    products = Post.query.all()
    product_schema = PostSchema(many=True)
    return product_schema.jsonify(products)

# Retrieve a specific product by ID endpoint
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = Post.query.get(product_id)
    product_schema = PostSchema()
    return product_schema.jsonify(product)

# Create a new product endpoint
@app.route('/api/products', methods=['POST'])
def create_product():
    title = request.json['title']
    body = request.json['body']
    user_id = request.json['user_id']
    post = Post(title=title, body=body, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    post_schema = PostSchema()
    return post_schema.jsonify(post)

# Update an existing product endpoint
@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Post.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    product.title = request.json.get('title', product.title)
    product.body = request.json.get('body', product.body)
    db.session.commit()
    product_schema = PostSchema()
    return product_schema.jsonify(product)

# Delete a product endpoint
@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Post.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'})

# Retrieve all products associated with a specific user endpoint
@app.route('/api/users/<int:user_id>/products', methods=['GET'])
@jwt_required()
def get_user_products(user_id):
    if user_id != get_jwt_identity():
        return jsonify({'error': 'Unauthorized'}), 401
    user = User.query.get(user_id)
    products = user.posts
    product_schema = PostSchema(many=True)
    return product_schema.jsonify(products)

# Associate a product with a specific user endpoint
@app.route('/api/users/<int:user_id>/products', methods=['POST'])
@jwt_required()
def add_user_product(user_id):
    if user_id != get_jwt_identity():
        return jsonify({'error': 'Unauthorized'}), 401
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    product_id = request.json['product_id']
    product = Post.query.get(product_id)
    
# Associate a product with a specific user endpoint
@app.route('/api/users/<int:user_id>/products', methods=['POST'])
@jwt_required()
def add_user_product(user_id):
    if user_id != get_jwt_identity():
        return jsonify({'error': 'Unauthorized'}), 401
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    product_id = request.json['product_id']
    product = Post.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    user.posts.append(product)
    db.session.commit()
    product_schema = PostSchema()
    return product_schema.jsonify(product)
if __name__ == '__main__':
    app.run(debug=True)
