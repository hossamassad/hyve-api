# app.py
from flask import Flask
from model.user import db
from model.product import db
from model.user_product import db
from controller.user_product_controller import api_bp
from controller.product_controller import product_bp
from controller.user_controller import user_bp
import instance.config as config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)