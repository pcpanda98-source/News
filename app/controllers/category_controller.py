from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.services.category_service import list_categories, create_category, update_category, delete_category, get_category

category_bp = Blueprint('categories', __name__, template_folder='templates')


@category_bp.route('/categories')
def categories_page():
    cats = list_categories()
    return render_template('categories.html', categories=cats)


@category_bp.route('/categories/manage', methods=['GET', 'POST'])
def manage_categories():
    if request.method == 'POST':
        name = request.form['name']
        create_category(name)
        return redirect(url_for('categories.manage_categories'))
    cats = list_categories()
    return render_template('manage_categories.html', categories=cats)


@category_bp.route('/api/categories', methods=['GET'])
def api_list_categories():
    """API endpoint to get all categories"""
    cats = list_categories()
    return jsonify([c.to_dict() for c in cats])


@category_bp.route('/api/categories/<int:cid>', methods=['PUT', 'DELETE'])
def api_modify_category(cid):
    if request.method == 'DELETE':
        ok = delete_category(cid)
        return ('', 204) if ok else ('Not found', 404)
    data = request.json
    c = update_category(cid, data.get('name'))
    return jsonify(c.to_dict()) if c else ('Not found', 404)
