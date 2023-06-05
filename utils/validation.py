from flask import jsonify

def validate_user_data(data):
    if not data.get('name'):
        return 'Name is required'
    if not data.get('email'):
        return 'Email is required'
    if not data.get('role'):
        return 'Role is required'
    if not data.get('password'):
        return 'Password is required'
    return None

def validate_product_data(data):
    if not data.get('name'):
        return 'Name is required'
    if not data.get('price'):
        return 'Price is required'
    if not isinstance(data.get('price'), (int, float)):
        return 'Price must be a number'
    return None

def validate_user_product_data(data):
    if not data.get('user_id'):
        return 'User ID is required'
    if not data.get('product_id'):
        return 'Product ID is required'
    return None