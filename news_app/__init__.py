from flask import Flask, send_from_directory, Response
from flask_compress import Compress
from .Backend.models.db import db
from .Backend.controllers.article_controller import article_bp
from .Backend.controllers.category_controller import category_bp
from .Backend.controllers.admin_controller import admin_bp
from .Backend.controllers.api_controller import api_bp
from .Backend.controllers.media_controller import media_bp
import os
import mimetypes

# Initialize compression
compress = Compress()

def create_app():
    template_dir = os.path.join(os.path.dirname(__file__), 'Frontend', 'templates')
    static_dir = os.path.join(os.path.dirname(__file__), 'Frontend', 'static')
    app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
    
    # Ensure correct MIME types
    mimetypes.add_type('text/css', '.css')
    mimetypes.add_type('application/javascript', '.js')
    
    # Performance: Configure compression
    app.config['COMPRESS_ENABLED'] = True
    app.config['COMPRESS_MIN_SIZE'] = 500  # Only compress responses > 500 bytes
    app.config['COMPRESS_BR_LEVEL'] = 6
    app.config['COMPRESS_GZIP_LEVEL'] = 6
    app.config['COMPRESS_EXCLUDE_PATHS'] = ['/static/uploads']  # Don't compress images
    
    # Initialize compression
    compress.init_app(app)
    
    # Configure SQLite database
    # Use persistent disk path on Render, local path for development
    disk_mount_path = os.getenv('DISK_MOUNT_PATH', '/opt/render/project/src')
    
    # Check if we're on Render (persistent disk exists)
    if os.path.exists(disk_mount_path):
        # Production: Use persistent disk for SQLite database
        db_path = os.path.join(disk_mount_path, 'news.db')
        print(f"[INFO] Using SQLite database on persistent disk: {db_path}")
    else:
        # Development: Use local file in project directory
        db_path = os.path.abspath('news.db')
        print(f"[INFO] Using local SQLite database: {db_path}")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {'timeout': 15, 'check_same_thread': False},
        'pool_pre_ping': True,
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')

    db.init_app(app)

    # Create tables and seed data within app context
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print(f"[INFO] Database tables initialized successfully")
            
            # Seed initial data if tables are empty
            from .Backend.seed import seed_data
            seed_data(app)
            
        except Exception as e:
            print(f"[WARNING] Database initialization error: {e}")
    
    app.register_blueprint(article_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(media_bp)

    return app

