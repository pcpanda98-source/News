from ..models.category import Category
from ..models.article import Article
from ..models.db import db

def list_categories():
    return Category.query.order_by(Category.id).all()

def get_category(cat_id):
    return db.session.get(Category, cat_id)

def create_category(name, description=None):
    c = Category(name=name, description=description)
    db.session.add(c)
    db.session.commit()
    return c

def update_category(cat_id, name, description=None):
    c = get_category(cat_id)
    if not c:
        return None
    c.name = name
    c.description = description
    db.session.commit()
    return c

def reorder_category_ids():
    """Reassign category IDs in ascending order starting from 1 to eliminate gaps"""
    categories = Category.query.order_by(Category.id).all()
    
    # Build old-to-new ID mapping FIRST (before modifying any category IDs)
    id_mapping = {}
    for index, category in enumerate(categories, start=1):
        old_id = category.id
        new_id = index
        id_mapping[old_id] = new_id
    
    # Update article references to match new category IDs BEFORE reassigning category IDs
    for old_id, new_id in id_mapping.items():
        if old_id != new_id:
            Article.query.filter_by(category_id=old_id).update({'category_id': new_id})
    
    # THEN reassign category IDs
    for index, category in enumerate(categories, start=1):
        category.id = index
    
    db.session.commit()

def delete_category(cat_id):
    c = get_category(cat_id)
    if not c:
        return False
    db.session.delete(c)
    db.session.commit()
    reorder_category_ids()
    return True

