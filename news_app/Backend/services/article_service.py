from ..models.article import Article
from ..models.db import db
from datetime import datetime, timezone
from sqlalchemy import func


def list_articles(page=1, per_page=12):
    """List articles with optional pagination"""
    if page and per_page:
        # Return paginated results with metadata
        pagination = Article.query \
            .order_by(Article.created_at.desc()) \
            .paginate(page=page, per_page=per_page, error_out=False)
        return {
            'items': pagination.items,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page,
            'per_page': pagination.per_page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    else:
        # Return all articles (legacy behavior)
        return Article.query.order_by(Article.created_at.desc()).all()


def list_articles_by_category(category_id, page=1, per_page=12):
    """List articles filtered by category ID with optional pagination"""
    if category_id:
        query = Article.query.filter_by(category_id=category_id)
    else:
        query = Article.query
    
    if page and per_page:
        pagination = query \
            .order_by(Article.created_at.desc()) \
            .paginate(page=page, per_page=per_page, error_out=False)
        return {
            'items': pagination.items,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page
        }
    else:
        return query.order_by(Article.created_at.desc()).all()


def count_articles():
    """Get total article count"""
    return Article.query.count()


def count_articles_today():
    """Count articles created today"""
    today = datetime.now().date()
    return Article.query.filter(func.date(Article.created_at) == today).count()


def count_articles_this_week():
    """Count articles created this week"""
    from datetime import timedelta
    week_ago = datetime.now() - timedelta(days=7)
    return Article.query.filter(Article.created_at >= week_ago).count()

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

def get_articles_by_ids(article_ids):
    """Get articles filtered by a list of IDs"""
    if not article_ids:
        return []
    return Article.query.filter(Article.id.in_(article_ids)).order_by(Article.created_at.desc()).all()

