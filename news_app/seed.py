from .models.db import db
from .models.article import Article
from .models.category import Category
from .services.category_service import create_category, list_categories
from .services.article_service import create_article, list_articles
from .services.media_service import list_media
from flask import Flask
import os

# Define standard categories that should always exist
STANDARD_CATEGORIES = [
    ('Technology', 'Latest technology news and updates'),
    ('World', 'Global news and international affairs'),
    ('Local', 'Local community news and events'),
    ('Business', 'Business and financial news'),
    ('Sports', 'Sports news and updates'),
    ('Entertainment', 'Movies, music, and celebrity news')
]

# Define standard articles
STANDARD_ARTICLES = [
    ('Welcome to Our News Platform', 
     'This is your comprehensive news management system. You can create, edit, and manage articles across different categories with media upload support.',
     'Local', 'Admin'),
    ('Latest Technology Trends 2024', 
     'Exploring the cutting-edge technology trends that are shaping our future. From AI advancements to sustainable tech solutions with media integration.',
     'Technology', 'Tech Editor'),
    ('Global Economic Outlook', 
     'An analysis of current global economic conditions and future projections for businesses worldwide. Categories help organize content effectively.',
     'Business', 'Business Analyst'),
    ('Community Events This Month', 
     'Stay updated with local community events, festivals, and activities. Media management makes sharing event photos easy.',
     'Local', 'Community Manager'),
    ('Breaking: Major Tech Announcement', 
     'A major technology company has just announced revolutionary changes to their platform. Industry experts are calling it a game-changer.',
     'Technology', 'Tech Reporter'),
    ('Sports Championship Results', 
     'The finals have concluded with an spectacular display of athletic prowess. Here are the complete results and highlights from the championship.',
     'Sports', 'Sports Desk')
]


def verify_seed_data():
    """
    Verify that the seed data exists and is correct.
    Returns: (is_valid, article_count, category_count)
    
    NOTE: This now only checks if the database has been initialized at all.
    User deletions are respected - deleted items stay deleted.
    """
    try:
        categories = list_categories()
        articles = list_articles()
        
        # Check if database has been initialized (has any data at all)
        # This allows user deletions to be permanent
        if len(categories) == 0 and len(articles) == 0:
            # Database is empty - needs initial seeding
            return False, 0, 0
        
        # Database has some data - user may have deleted some items
        # We respect their deletions and don't auto-reseed
        print(f'[INFO] Database has {len(articles)} articles and {len(categories)} categories (user deletions respected)')
        return True, len(articles), len(categories)
        
    except Exception as e:
        print(f'[ERROR] Error verifying seed data: {e}')
        return False, 0, 0


def ensure_categories_exist(categories_to_create):
    """
    Ensure all required categories exist, creating any that are missing.
    This respects user deletions - if a category was deleted, it won't be recreated.
    Returns a dictionary mapping category names to category objects.
    """
    existing_cats = list_categories()
    cat_map = {c.name: c for c in existing_cats}
    
    # Only create categories if we have none at all (first initialization)
    if not cat_map:
        for name, desc in categories_to_create:
            try:
                cat = create_category(name, desc)
                cat_map[name] = cat
                print(f'[INFO] Created initial category: {name}')
            except Exception as e:
                print(f'[ERROR] Failed to create category {name}: {e}')
    
    return cat_map


def seed_data(app=None, force=False):
    """
    Seed the database with initial data if it doesn't exist.
    
    Args:
        app: Flask application instance
        force: If True, recreate all seed data even if it exists
    
    This function respects user deletions. If users delete articles or categories,
    they stay deleted. Only --force flag or empty database will trigger reseeding.
    """
    if app is None:
        from . import create_app
        app = create_app()
    
    with app.app_context():
        try:
            # Check current state
            existing_cats = list_categories()
            existing_articles = list_articles()
            
            if force:
                print('[INFO] Force seeding - clearing existing data...')
                # Delete all existing articles and categories
                Article.query.delete()
                Category.query.delete()
                db.session.commit()
                existing_cats = []
                existing_articles = []
            
            # Verify seed data exists
            is_valid, article_count, category_count = verify_seed_data()
            
            if is_valid and existing_cats and existing_articles:
                print(f'[INFO] Database already properly seeded. Articles: {article_count}, Categories: {category_count}')
                return True
            
            # If we get here, database is empty and needs initial seeding
            print('[INFO] Database is empty. Seeding initial data...')
            
            # Ensure upload directory exists
            upload_dir = 'static/uploads'
            os.makedirs(upload_dir, exist_ok=True)
            gitkeep_path = os.path.join(upload_dir, '.gitkeep')
            if not os.path.exists(gitkeep_path):
                with open(gitkeep_path, 'w') as f:
                    f.write('# Keep this directory in git\n')
            
            # Ensure all categories exist (only if empty)
            cat_map = ensure_categories_exist(STANDARD_CATEGORIES)
            
            # Create sample articles (only if none exist)
            current_article_count = Article.query.count()
            if current_article_count == 0:
                print('[INFO] Creating initial sample articles...')
                
                for title, content, cat_name, author in STANDARD_ARTICLES:
                    cat = cat_map.get(cat_name)
                    try:
                        create_article(title, content, cat.id if cat else None, author)
                        print(f'[INFO] Created article: {title}')
                    except Exception as e:
                        print(f'[ERROR] Failed to create article {title}: {e}')
            else:
                print(f'[INFO] Database has {current_article_count} articles (user deletions respected)')
            
            # Commit changes to ensure persistence
            try:
                db.session.commit()
            except Exception as commit_error:
                db.session.rollback()
                print(f'[WARNING] Commit warning: {commit_error}')
            
            # Final verification
            final_articles = Article.query.count()
            final_categories = Category.query.count()
            
            print(f'[SUCCESS] Database initialized! Articles: {final_articles}, Categories: {final_categories}')
            
            return True
            
        except Exception as e:
            print(f'[ERROR] Error seeding database: {e}')
            import traceback
            traceback.print_exc()
            return False


def create_app_with_seeding():
    """
    Create Flask app with automatic database seeding.
    This is an alternative to create_app() that ensures data persistence.
    """
    from . import create_app
    
    app = create_app()
    
    # Seed data on startup
    with app.app_context():
        seed_data(app)
    
    return app


if __name__ == '__main__':
    import sys
    
    # Check for force flag
    force = '--force' in sys.argv
    
    # Run seeding when executed directly
    success = seed_data(force=force)
    if success:
        print('[SUCCESS] Seeding completed successfully!')
    else:
        print('[FAILED] Seeding failed. Check errors above.')

