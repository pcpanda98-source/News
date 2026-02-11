from flask import Blueprint, render_template
from ..services.article_service import list_articles
from ..services.category_service import list_categories
from ..services.media_service import list_media

admin_bp = Blueprint('admin', __name__, template_folder='templates')


@admin_bp.route('/admin')
def dashboard():
    articles = list_articles()
    categories = list_categories()
    return render_template('admin_dashboard.html', articles=articles, categories=categories)


@admin_bp.route('/manage')
def manage_articles():
    """Manage articles page"""
    articles = list_articles()
    categories = list_categories()
    return render_template('manage_articles.html', articles=articles, categories=categories)


@admin_bp.route('/bookmarks')
def bookmarks():
    """Bookmarks page"""
    articles = list_articles()
    return render_template('bookmarks.html', articles=articles)

