from database import db

class UserProducts(db.Model):
    __tablename__ = 'user_products'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)

    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id

    def __repr__(self):
        return f"<UserProduct {self.user_id} - {self.product_id}>"

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'product_id': self.product_id
        }