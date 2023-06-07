from flask import Flask
from instance import config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

from controller.user_controller import user_bp
from controller.product_controller import product_bp
from controller.user_product_controller import api_bp

app.register_blueprint(user_bp)
app.register_blueprint(product_bp)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)
