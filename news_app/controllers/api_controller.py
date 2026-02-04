from flask import Blueprint, jsonify, request
from ..services.news_service import top_headlines, search_news, get_sources
from ..models.db import db
from ..services.article_service import list_articles
from ..services.category_service import list_categories
import os

api_bp = Blueprint('api', __name__)


@api_bp.route('/live')
def live_news():
    """Get top headlines with optional country and category filters"""
    country = request.args.get('country', 'us')
    category = request.args.get('category')
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    
    data = top_headlines(country=country, category=category, page=page, page_size=page_size)
    return jsonify(data)


@api_bp.route('/search')
def search():
    """Search for news articles by keyword"""
    query = request.args.get('q', '')
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    sort_by = request.args.get('sortBy', 'publishedAt')
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    
    if not query:
        return jsonify({'status': 'error', 'message': 'Query parameter is required', 'articles': []}), 400
    
    data = search_news(
        query=query,
        from_date=from_date,
        to_date=to_date,
        sort_by=sort_by,
        page=page,
        page_size=page_size
    )
    return jsonify(data)


@api_bp.route('/sources')
def sources():
    """Get available news sources"""
    data = get_sources()
    return jsonify(data)


@api_bp.route('/health')
def health():
    """Health check endpoint with database status"""
    # Check database connection
    db_status = 'unknown'
    db_url = os.getenv('DATABASE_URL', '')
    article_count = 0
    category_count = 0
    
    try:
        # Check if using PostgreSQL or SQLite
        if db_url.startswith('postgresql'):
            db_type = 'PostgreSQL'
        elif db_url.startswith('postgres'):
            db_type = 'PostgreSQL (legacy)'
        elif db_url:
            db_type = 'SQLite'
        else:
            db_type = 'SQLite (default)'
        
        # Test database connection and get counts
        articles = list_articles()
        categories = list_categories()
        article_count = len(articles)
        category_count = len(categories)
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'
        db_type = 'unknown'
    
    return jsonify({
        'status': 'healthy',
        'message': 'API is running',
        'database': {
            'status': db_status,
            'type': db_type,
            'url_set': bool(db_url),
            'article_count': article_count,
            'category_count': category_count
        }
    })

