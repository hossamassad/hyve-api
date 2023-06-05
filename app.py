from flask import Flask
from instance.config import Config
from database import db
from api import (
    users,
    products,
    user_products
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(products)
    app.register_blueprint(user_products)

    return app 

