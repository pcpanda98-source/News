from app.models.article import Article
from app.models.db import db

def list_articles():
    return Article.query.order_by(Article.created_at.desc()).all()

def get_article(article_id):
    return Article.query.get(article_id)

def create_article(title, content, category_id=None, image_url=None):
    a = Article(title=title, content=content, category_id=category_id, image_url=image_url)
    db.session.add(a)
    db.session.commit()
    return a

def update_article(article_id, title, content, category_id=None, image_url=None):
    a = get_article(article_id)
    if not a:
        return None
    a.title = title
    a.content = content
    a.category_id = category_id
    a.image_url = image_url
    db.session.commit()
    return a

def delete_article(article_id):
    a = get_article(article_id)
    if not a:
        return False
    db.session.delete(a)
    db.session.commit()
    return True
