from flask import Blueprint, jsonify, request, current_app
from ..services.news_service import top_headlines, search_news, get_sources
from ..models.db import db
from ..services.article_service import list_articles
from ..services.category_service import list_categories
import os
import hashlib
import time

api_bp = Blueprint('api', __name__)

# Cache configuration for API endpoints
CACHE_TIMEOUT_LIVE = 300  # 5 minutes for live news
CACHE_TIMEOUT_SEARCH = 600  # 10 minutes for search results
CACHE_TIMEOUT_SOURCES = 3600  # 1 hour for sources (rarely change)

# In-memory cache storage
_api_cache = {}


def _get_cache_key(prefix, **kwargs):
    """Generate a cache key from request parameters"""
    sorted_params = sorted(kwargs.items())
    params_str = '&'.join(f'{k}={v}' for k, v in sorted_params if v)
    key_str = f'{prefix}:{params_str}'
    return hashlib.md5(key_str.encode()).hexdigest()


def _get_cached_response(cache_key, timeout):
    """Get cached response if still valid"""
    if cache_key in _api_cache:
        cached_time, response_data = _api_cache[cache_key]
        if time.time() - cached_time < timeout:
            return response_data
    return None


def _set_cached_response(cache_key, response_data, timeout):
    """Store response in cache"""
    _api_cache[cache_key] = (time.time(), response_data)


def clear_api_cache():
    """Clear all API cache"""
    global _api_cache
    _api_cache = {}


@api_bp.route('/live')
def live_news():
    """Get top headlines with optional country and category filters"""
    country = request.args.get('country', 'us')
    category = request.args.get('category')
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    
    # Check for no-cache parameter
    no_cache = request.args.get('no_cache') == '1'
    
    if not no_cache:
        # Try to get from cache
        cache_key = _get_cache_key('live', country=country, category=category, page=page, page_size=page_size)
        cached = _get_cached_response(cache_key, CACHE_TIMEOUT_LIVE)
        if cached:
            return jsonify(cached)
    
    # Fetch from external API
    data = top_headlines(country=country, category=category, page=page, page_size=page_size)
    
    # Cache the response
    if not no_cache:
        _set_cached_response(cache_key, data, CACHE_TIMEOUT_LIVE)
    
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
    
    # Check for no-cache parameter
    no_cache = request.args.get('no_cache') == '1'
    
    if not no_cache:
        # Try to get from cache
        cache_key = _get_cache_key('search', q=query, from_date=from_date, to_date=to_date, sort_by=sort_by, page=page, page_size=page_size)
        cached = _get_cached_response(cache_key, CACHE_TIMEOUT_SEARCH)
        if cached:
            return jsonify(cached)
    
    # Fetch from external API
    data = search_news(
        query=query,
        from_date=from_date,
        to_date=to_date,
        sort_by=sort_by,
        page=page,
        page_size=page_size
    )
    
    # Cache the response
    if not no_cache:
        _set_cached_response(cache_key, data, CACHE_TIMEOUT_SEARCH)
    
    return jsonify(data)


@api_bp.route('/sources')
def sources():
    """Get available news sources"""
    # Check for no-cache parameter
    no_cache = request.args.get('no_cache') == '1'
    
    if not no_cache:
        # Try to get from cache
        cache_key = _get_cache_key('sources')
        cached = _get_cached_response(cache_key, CACHE_TIMEOUT_SOURCES)
        if cached:
            return jsonify(cached)
    
    # Fetch from external API
    data = get_sources()
    
    # Cache the response
    if not no_cache:
        _set_cached_response(cache_key, data, CACHE_TIMEOUT_SOURCES)
    
    return jsonify(data)


@api_bp.route('/clear-cache', methods=['POST'])
def clear_cache_endpoint():
    """Clear API cache (admin endpoint)"""
    try:
        clear_api_cache()
        return jsonify({'status': 'success', 'message': 'Cache cleared successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


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

