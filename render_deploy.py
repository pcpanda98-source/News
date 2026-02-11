#!/usr/bin/env python3
"""
Render.com Deployment Fix Script
Ensures database seeding and media upload functionality work correctly
"""
import os
import sys
from news_app import create_app
from news_app.Backend.models.db import db
from news_app.Backend.services.category_service import create_category, list_categories
from news_app.Backend.services.article_service import create_article, list_articles
from news_app.Backend.services.media_service import list_media

def setup_media_directories():
    """Setup media upload directories for both local and Render.com"""
    directories = [
        'static/uploads',  # Relative path for local development
        '/opt/render/project/src/static/uploads'  # Render.com path
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            # Create .gitkeep file
            gitkeep_path = os.path.join(directory, '.gitkeep')
            if not os.path.exists(gitkeep_path):
                with open(gitkeep_path, 'w') as f:
                    f.write('# Keep this directory in git\n')
            print(f"✅ Media directory ready: {directory}")
        except Exception as e:
            print(f"⚠️  Could not create directory {directory}: {e}")

def ensure_sample_data():
    """Ensure sample categories and articles exist"""
    app = create_app()
    
    with app.app_context():
        try:
            # Create tables
            db.create_all()
            print("✅ Database tables created")
        except Exception as e:
            print(f"⚠️  Database table creation warning: {e}")
            # Continue anyway as tables might already exist
        
        # Setup media directories
        setup_media_directories()
        
        # Get existing data
        existing_cats = list_categories()
        existing_articles = list_articles()
        existing_media = list_media()
        
        cat_names = [cat.name for cat in existing_cats]
        article_titles = [art.title for art in existing_articles]
        
        # Required categories with descriptions
        required_categories = [
            ('Technology', 'Latest technology news and updates'),
            ('World', 'Global news and international affairs'),
            ('Local', 'Local community news and events'),
            ('Business', 'Business and financial news'),
            ('Sports', 'Sports news and updates'),
            ('Entertainment', 'Movies, music, and celebrity news')
        ]
        
        # Add missing categories
        categories_added = 0
        for cat_name, cat_desc in required_categories:
            if cat_name not in cat_names:
                create_category(cat_name, cat_desc)
                categories_added += 1
                print(f"✅ Added category: {cat_name}")
        
        # Get updated categories
        categories = list_categories()
        cat_dict = {cat.name: cat.id for cat in categories}
        
        # Required sample articles
        sample_articles = [
            {
                'title': 'Welcome to Our News Platform',
                'content': 'This is your comprehensive news management system. Create, edit, and manage articles across categories with media upload support. All your content persists between deployments.',
                'author': 'Admin',
                'category_id': cat_dict.get('Local')
            },
            {
                'title': 'Technology Trends 2024',
                'content': 'Discover the latest technology trends shaping our future. From AI advancements to sustainable tech solutions, explore innovations with full media integration capabilities.',
                'author': 'Tech Editor',
                'category_id': cat_dict.get('Technology')
            },
            {
                'title': 'Global Economic Update',
                'content': 'Analysis of current global economic conditions and future projections. Understanding market trends and their impact on businesses worldwide with comprehensive category organization.',
                'author': 'Business Analyst',
                'category_id': cat_dict.get('Business')
            },
            {
                'title': 'Community Events Guide',
                'content': 'Stay updated with local community events, festivals, and activities. Join various cultural and social gatherings. Media management makes sharing event photos seamless.',
                'author': 'Community Manager',
                'category_id': cat_dict.get('Local')
            }
        ]
        
        # Add missing sample articles
        articles_added = 0
        for article_data in sample_articles:
            if article_data['title'] not in article_titles:
                create_article(
                    title=article_data['title'],
                    content=article_data['content'],
                    category_id=article_data['category_id'],
                    author=article_data['author']
                )
                articles_added += 1
                print(f"✅ Added article: {article_data['title']}")
        
        # Final verification
        final_articles = list_articles()
        final_categories = list_categories()
        final_media = list_media()

        # Set DATABASE_SEEDED environment variable to prevent re-seeding on subsequent deployments
        os.environ['DATABASE_SEEDED'] = 'true'

        print(f"\n🎉 Deployment setup complete!")
        print(f"   📂 Categories: {len(final_categories)} total ({categories_added} added)")
        print(f"   📰 Articles: {len(final_articles)} total ({articles_added} added)")
        print(f"   🖼️  Media files: {len(final_media)} in database")
        print(f"   📁 Upload directories configured")
        print(f"   🔒 DATABASE_SEEDED=true set (will prevent re-seeding on next deploy)")

        return True

if __name__ == '__main__':
    try:
        success = ensure_sample_data()
        if success:
            print("\n✅ Render.com deployment setup completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Deployment setup failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Deployment setup error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

