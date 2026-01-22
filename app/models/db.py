from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    from app.models.article import Article
    from app.models.category import Category
    from app.models.media import Media
    db.create_all()
