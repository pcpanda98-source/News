# app package
from flask import Flask
from app.models.db import db, init_db
from app.controllers.article_controller import article_bp
from app.controllers.category_controller import category_bp
from app.controllers.admin_controller import admin_bp
from app.controllers.api_controller import api_bp
from app.controllers.media_controller import media_bp
import os

def create_app():
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
    app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
    
    # Use absolute path for database to ensure persistence
    if os.getenv('DATABASE_URL'):
        db_uri = os.getenv('DATABASE_URL')
    else:
        instance_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance'))
        os.makedirs(instance_path, exist_ok=True)
        db_path = os.path.join(instance_path, 'news.db')
        # Use proper SQLite URI format for absolute paths
        db_uri = 'sqlite:///' + db_path
    
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')

    db.init_app(app)
    with app.app_context():
        init_db()

    app.register_blueprint(article_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(media_bp)

    return app
