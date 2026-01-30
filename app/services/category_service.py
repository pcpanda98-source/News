from app.models.category import Category
from app.models.db import db

def list_categories():
    return Category.query.order_by(Category.id).all()

def get_category(cat_id):
    return db.session.get(Category, cat_id)

def create_category(name):
    c = Category(name=name)
    db.session.add(c)
    db.session.commit()
    return c

def update_category(cat_id, name):
    c = get_category(cat_id)
    if not c:
        return None
    c.name = name
    db.session.commit()
    return c

def delete_category(cat_id):
    c = get_category(cat_id)
    if not c:
        return False
    db.session.delete(c)
    db.session.commit()
    return True

