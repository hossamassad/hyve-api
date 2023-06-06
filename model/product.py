from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

db = SQLAlchemy()

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