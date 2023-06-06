from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from model.product import db, Product


def get_all_products(page=1, per_page=10):
    products = Product.query.paginate(page=page, per_page=per_page, error_out=False)
    return [product.to_dict() for product in products.items]

def get_product(product_id):
    try:
        product = Product.query.filter_by(id=product_id).one()
        return product.to_dict()
    except NoResultFound:
        return {'error': 'Product not found'}

def add_product(name, price):
    try:
        product = Product(name=name, price=price)
        db.session.add(product)
        db.session.commit()
        return product.to_dict()
    except IntegrityError:
        db.session.rollback()
        return {'error': 'Product already exists'}

def update_product(product_id, name=None, price=None):
    try:
        product = Product.query.filter_by(id=product_id).one()
        if name:
            product.name = name
        if price:
            product.price = price
        db.session.commit()
        return product.to_dict()
    except NoResultFound:
        return {'error': 'Product not found'}

def delete_product(product_id):
    try:
        product = Product.query.filter_by(id=product_id).one()
        db.session.delete(product)
        db.session.commit()
        return None
    except NoResultFound:
        return {'error': 'Product not found'}