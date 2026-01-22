from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.services.article_service import list_articles, get_article, create_article, update_article, delete_article
from app.services.category_service import list_categories

article_bp = Blueprint('articles', __name__, template_folder='templates')


@article_bp.route('/')
def home():
    # show live news page is primary; but also show internal articles
    articles = list_articles()
    categories = list_categories()
    return render_template('index.html', articles=articles, categories=categories)


@article_bp.route('/articles')
def articles_page():
    articles = list_articles()
    return render_template('articles.html', articles=articles)


@article_bp.route('/live')
def live_news():
    news_api_key = 'pub_b6ea65c0579b42b5a8f61d11f2eac14f'
    return render_template('live_news.html', news_api_key=news_api_key)


@article_bp.route('/articles/create', methods=['GET', 'POST'])
def create_article_page():
    categories = list_categories()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category_id = request.form.get('category') or None
        create_article(title, content, category_id)
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
    a = update_article(aid, data.get('title'), data.get('content'), data.get('category_id'))
    return jsonify(a.to_dict()) if a else ('Not found', 404)
