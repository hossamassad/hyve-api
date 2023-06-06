from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from model.user import db, User

def get_all_users(page=1, per_page=10):
    users = User.query.paginate(page=page, per_page=per_page, error_out=False)
    return [user.to_dict() for user in users.items]

def get_user(user_id):
    try:
        user = User.query.filter_by(id=user_id).one()
        return user.to_dict()
    except NoResultFound:
        return {'error': 'User not found'}

def add_user(name, email):
    try:
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return user.to_dict()
    except IntegrityError:
        db.session.rollback()
        return {'error': 'Email already exists'}

def update_user(user_id, name=None, email=None):
    try:
        user = User.query.filter_by(id=user_id).one()
        if name:
            user.name = name
        if email:
            user.email = email
        db.session.commit()
        return user.to_dict()
    except NoResultFound:
        return {'error': 'User not found'}

def delete_user(user_id):
    try:
        user = User.query.filter_by(id=user_id).one()
        db.session.delete(user)
        db.session.commit()
        return None
    except NoResultFound:
        return {'error': 'User not found'}
