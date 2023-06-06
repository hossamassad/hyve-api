from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from model.product import db, Product
from model.user import db, User
from model.user_product import db,UserProduct
def get_user_products(user_id):
    try:
        user = User.query.filter_by(id=user_id).one()
        user_products = user.products
        return [product.to_dict() for product in user_products]
    except NoResultFound:
        return {'error': 'User not found'}

def add_user_product(user_id, product_id):
    try:
        user_product = UserProduct(user_id=user_id, product_id=product_id)
        db.session.add(user_product)
        db.session.commit()
        return user_product.to_dict()
    except IntegrityError:
        db.session.rollback()
        return {'error': 'User already has this product'}

def delete_user_product(user_id, product_id):
    try:
        user_product = UserProduct.query.filter_by(user_id=user_id, product_id=product_id).one()
        db.session.delete(user_product)
        db.session.commit()
        return None
    except NoResultFound:
        return {'error': 'User-Product association not found'}