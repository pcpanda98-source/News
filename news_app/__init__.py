from flask import Flask, send_from_directory
from flask_compress import Compress
from .Backend.models.db import db
from .Backend.controllers.article_controller import article_bp
from .Backend.controllers.category_controller import category_bp
from .Backend.controllers.admin_controller import admin_bp
from .Backend.controllers.api_controller import api_bp
from .Backend.controllers.media_controller import media_bp
import os

compress = Compress()

def create_app():
    template_dir = os.path.join(os.path.dirname(__file__), 'Frontend', 'templates')
    static_dir = os.path.join(os.path.dirname(__file__), 'Frontend', 'static')
    app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
    
    app.config['COMPRESS_ENABLED'] = True
    compress.init_app(app)
    
    # Database configuration
    disk_mount = os.getenv('DISK_MOUNT_PATH', '/opt/render/project/src')
    if os.path.exists(disk_mount):
        db_path = os.path.join(disk_mount, 'news.db')
    else:
        db_path = os.path.abspath('news.db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')

    db.init_app(app)

    with app.app_context():
        try:
            db.create_all()
            from .Backend.seed import seed_data
            seed_data(app)
        except Exception as e:
            print(f"[ERROR] Init failed: {e}")
    
    app.register_blueprint(article_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(media_bp)

    return app

