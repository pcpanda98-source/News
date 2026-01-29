from flask import Flask
from app.models.db import db
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
    
    # Configure persistent SQLite database
    if os.getenv('DATABASE_URL'):
        db_uri = os.getenv('DATABASE_URL')
    else:
        # Use current working directory for database - ensures persistence
        db_path = os.path.abspath('news.db')
        db_uri = f'sqlite:///{db_path}'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
    # Ensure database connections are persistent
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {'timeout': 15, 'check_same_thread': False},
        'pool_pre_ping': True,  # Verify connections before using them
    }

    db.init_app(app)

    # Create tables within app context (only creates if they don't exist)
    with app.app_context():
        db.create_all()
        print(f"[INFO] Database initialized at: {db_uri}")
    
    app.register_blueprint(article_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(media_bp)

    return app

