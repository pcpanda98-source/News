from flask import Flask
from app.models.db import db, init_db
from app.controllers.article_controller import article_bp
from app.controllers.category_controller import category_bp
from app.controllers.admin_controller import admin_bp
from app.controllers.api_controller import api_bp
import os

def create_app():
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
    app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///news.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')

    db.init_app(app)
    with app.app_context():
        init_db()

    app.register_blueprint(article_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    cert = os.getenv('SSL_CERT')
    key = os.getenv('SSL_KEY')
    if cert and key:
        app.run(host='0.0.0.0', port=8443, ssl_context=(cert, key), debug=True)
    else:
        app.run(host='0.0.0.0', port=8080, debug=True)
