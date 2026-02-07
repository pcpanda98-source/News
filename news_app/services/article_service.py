from ..models.article import Article
from ..models.db import db
from datetime import datetime, timezone


def list_articles():
    return Article.query.order_by(Article.created_at.desc()).all()

def list_articles_by_category(category_id):
    """List articles filtered by category ID"""
    if category_id:
        return Article.query.filter_by(category_id=category_id).order_by(Article.created_at.desc()).all()
    return Article.query.order_by(Article.created_at.desc()).all()

def get_article(article_id):
    return db.session.get(Article, article_id)

def create_article(title, content, category_id=None, image_url=None, author=None):
    a = Article(title=title, author=author, content=content, category_id=category_id, image_url=image_url)
    db.session.add(a)
    db.session.commit()
    return a

def update_article(article_id, title, content, category_id=None, image_url=None, author=None):
    a = get_article(article_id)
    if not a:
        return None
    a.title = title
    a.author = author
    a.content = content
    a.category_id = category_id
    a.image_url = image_url
    db.session.commit()
    return a

def reorder_article_ids():
    """Reassign article IDs in ascending order starting from 1 to eliminate gaps"""
    articles = Article.query.order_by(Article.id).all()
    for index, article in enumerate(articles, start=1):
        article.id = index
    db.session.commit()

def delete_article(article_id):
    a = get_article(article_id)
    if not a:
        return False
    db.session.delete(a)
    db.session.commit()
    reorder_article_ids()
    return True

