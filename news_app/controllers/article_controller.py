from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from ..services.article_service import list_articles, list_articles_by_category, get_article, create_article, update_article, delete_article
from ..services.category_service import list_categories, get_category

article_bp = Blueprint('articles', __name__, template_folder='templates')


@article_bp.route('/')
def home():
    # show live news page is primary; but also show internal articles
    articles = list_articles()
    categories = list_categories()
    return render_template('index.html', articles=articles, categories=categories)


@article_bp.route('/articles')
def articles_page():
    category_param = request.args.get('category')
    search_term = request.args.get('search')
    
    selected_category = ''
    
    if category_param:
        # First try to find category by ID (if parameter is numeric)
        if category_param.isdigit():
            category = get_category(int(category_param))
            if category:
                articles = list_articles_by_category(category.id)
                selected_category = category.name
            else:
                articles = list_articles()
                selected_category = ''
        else:
            # Try to find category by name
            categories = list_categories()
            category = next((cat for cat in categories if cat.name == category_param), None)
            if category:
                articles = list_articles_by_category(category.id)
                selected_category = category.name
            else:
                articles = list_articles()
                selected_category = ''
    else:
        articles = list_articles()
        selected_category = ''
    
    categories = list_categories()
    return render_template('articles.html', 
                         articles=articles, 
                         categories=categories, 
                         selected_category=selected_category,
                         search_term=search_term or '')


@article_bp.route('/latest')
def latest_news():
    """Show latest created news articles with timestamps"""
    articles = list_articles()
    categories = list_categories()
    return render_template('latest.html', articles=articles, categories=categories)


@article_bp.route('/live-feed')
def live_feed():
    """Show live news feed from external API"""
    news_api_key = '7ee335fefcc3490982cb790ed9f85c8a'
    return render_template('live_news.html', news_api_key=news_api_key)


@article_bp.route('/bookmarks')
def bookmarks_page():
    """Show user's bookmarked articles"""
    articles = list_articles()
    categories = list_categories()
    return render_template('bookmarks.html', articles=articles, categories=categories)


@article_bp.route('/articles/create', methods=['GET', 'POST'])
def create_article_page():
    categories = list_categories()
    if request.method == 'POST':
        title = request.form['title']
        author = request.form.get('author') or None
        content = request.form['content']
        image_url = request.form.get('image_url') or None
        category_id = request.form.get('category') or None
        create_article(title, content, category_id, image_url, author)
        return redirect(url_for('articles.articles_page'))
    return render_template('create_article.html', categories=categories)


@article_bp.route('/articles/<int:article_id>')
def article_detail(article_id):
    a = get_article(article_id)
    if not a:
        return 'Not found', 404
    return render_template('article_detail.html', article=a)


@article_bp.route('/manage')
def manage_articles():
    articles = list_articles()
    categories = list_categories()
    return render_template('manage_articles.html', articles=articles, categories=categories)


@article_bp.route('/api/articles')
def api_list_articles():
    articles = [a.to_dict() for a in list_articles()]
    return jsonify(articles)


@article_bp.route('/api/articles/<int:aid>', methods=['PUT', 'DELETE'])
def api_modify_article(aid):
    if request.method == 'DELETE':
        ok = delete_article(aid)
        return ('', 204) if ok else ('Not found', 404)
    data = request.json
    a = update_article(aid, data.get('title'), data.get('content'), data.get('category_id'), data.get('image_url'), data.get('author'))
    return jsonify(a.to_dict()) if a else ('Not found', 404)

