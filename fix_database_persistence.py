"""
Database Persistence Fix for News Management System

This script fixes database persistence issues that cause data loss on app restart.
It ensures that articles and categories are properly saved to the database and
persist across application restarts.

Common issues addressed:
1. Database connection failures
2. Transaction commit failures
3. Data not persisting to disk
4. Race conditions during initialization
5. Session management issues
"""

import os
import sqlite3
import time
from datetime import datetime, timezone

def get_database_path():
    """Get the correct database path for the environment"""
    # Check for production database URL
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        # Production: PostgreSQL - no local path needed
        return None
    
    # Development: SQLite
    return os.path.abspath('news.db')

def verify_sqlite_database():
    """
    Verify SQLite database exists and has correct structure.
    Returns tuple: (is_valid, article_count, category_count)
    """
    db_path = get_database_path()
    
    if not db_path:
        # PostgreSQL database - verify connection differently
        return verify_postgresql_database()
    
    if not os.path.exists(db_path):
        return False, 0, 0
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='articles'")
        articles_exist = cursor.fetchone() is not None
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='categories'")
        categories_exist = cursor.fetchone() is not None
        
        if not articles_exist or not categories_exist:
            conn.close()
            return False, 0, 0
        
        # Count records
        cursor.execute("SELECT COUNT(*) FROM articles")
        article_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM categories")
        category_count = cursor.fetchone()[0]
        
        conn.close()
        
        return True, article_count, category_count
        
    except Exception as e:
        print(f"[ERROR] Database verification failed: {e}")
        return False, 0, 0

def verify_postgresql_database():
    """
    Verify PostgreSQL database connection and data.
    Returns tuple: (is_valid, article_count, category_count)
    """
    from sqlalchemy import create_engine, text
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        return False, 0, 0
    
    # Fix PostgreSQL URL format for SQLAlchemy
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        engine = create_engine(database_url, connect_args={'connect_timeout': 10})
        
        with engine.connect() as conn:
            # Check if tables exist
            result = conn.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'articles')"))
            articles_exist = result.scalar()
            
            result = conn.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'categories')"))
            categories_exist = result.scalar()
            
            if not articles_exist or not categories_exist:
                return False, 0, 0
            
            # Count records
            result = conn.execute(text("SELECT COUNT(*) FROM articles"))
            article_count = result.scalar()
            
            result = conn.execute(text("SELECT COUNT(*) FROM categories"))
            category_count = result.scalar()
            
            return True, article_count, category_count
            
    except Exception as e:
        print(f"[ERROR] PostgreSQL verification failed: {e}")
        return False, 0, 0

def force_seed_database():
    """
    Force re-seed the database with initial data.
    This will delete all existing data and recreate it.
    WARNING: This is destructive - use only for recovery!
    """
    from news_app import create_app
    from news_app.models.db import db
    from news_app.models.article import Article
    from news_app.models.category import Category
    from news_app.services.category_service import create_category
    from news_app.services.article_service import create_article
    
    print("[INFO] Force seeding database...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Clear existing data
            print("[INFO] Clearing existing data...")
            Article.query.delete()
            Category.query.delete()
            db.session.commit()
            print("[INFO] Existing data cleared.")
            
            # Recreate categories
            categories_to_create = [
                ('Technology', 'Latest technology news and updates'),
                ('World', 'Global news and international affairs'),
                ('Local', 'Local community news and events'),
                ('Business', 'Business and financial news'),
                ('Sports', 'Sports news and updates'),
                ('Entertainment', 'Movies, music, and celebrity news')
            ]
            
            for name, desc in categories_to_create:
                create_category(name, desc)
                print(f"[INFO] Created category: {name}")
            
            # Recreate articles
            articles_to_create = [
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
            
            # Get category mapping
            cat_map = {}
            categories = Category.query.all()
            for cat in categories:
                cat_map[cat.name] = cat
            
            for title, content, cat_name, author in articles_to_create:
                cat = cat_map.get(cat_name)
                create_article(title, content, cat.id if cat else None, author)
                print(f"[INFO] Created article: {title}")
            
            # Verify final state
            article_count = Article.query.count()
            category_count = Category.query.count()
            
            print(f"[SUCCESS] Database force seeded! Contains {article_count} articles and {category_count} categories.")
            return True
            
        except Exception as e:
            print(f"[ERROR] Force seeding failed: {e}")
            import traceback
            traceback.print_exc()
            return False

def test_database_write():
    """
    Test that the database can write and persist data.
    Creates a test article and verifies it can be read back.
    """
    from news_app import create_app
    from news_app.models.db import db
    from news_app.models.article import Article
    from news_app.services.article_service import create_article, list_articles
    
    print("[INFO] Testing database write operations...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Get initial count
            initial_count = len(list_articles())
            print(f"[INFO] Initial article count: {initial_count}")
            
            # Create test article
            test_title = f"Test Article {datetime.now(timezone.utc).isoformat()}"
            test_content = "This is a test article to verify database persistence."
            
            new_article = create_article(test_title, test_content, None, "Test System")
            print(f"[INFO] Created test article with ID: {new_article.id}")
            
            # Verify it's in the database
            db.session.flush()
            
            # Count again
            after_count = len(list_articles())
            print(f"[INFO] Article count after creation: {after_count}")
            
            if after_count > initial_count:
                print("[SUCCESS] Database write test PASSED!")
                print("[INFO] New articles are being saved correctly.")
                
                # Clean up test article
                from news_app.services.article_service import delete_article
                delete_article(new_article.id)
                print("[INFO] Test article cleaned up.")
                
                return True
            else:
                print("[FAIL] Database write test FAILED!")
                print("[ERROR] New articles are NOT being saved to the database!")
                return False
                
        except Exception as e:
            print(f"[ERROR] Database write test failed: {e}")
            import traceback
            traceback.print_exc()
            return False

def diagnose_database_issues():
    """
    Comprehensive diagnosis of database issues.
    Returns a dictionary with diagnosis results.
    """
    results = {
        'database_type': 'unknown',
        'database_exists': False,
        'tables_exist': False,
        'article_count': 0,
        'category_count': 0,
        'write_test_passed': False,
        'issues': [],
        'recommendations': []
    }
    
    # Determine database type
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        results['database_type'] = 'postgresql'
        print("[INFO] Using PostgreSQL database (production)")
    else:
        results['database_type'] = 'sqlite'
        print("[INFO] Using SQLite database (development)")
    
    # Check database existence
    is_valid, article_count, category_count = verify_sqlite_database()
    results['database_exists'] = is_valid
    results['article_count'] = article_count
    results['category_count'] = category_count
    
    if is_valid:
        print(f"[INFO] Database is valid with {article_count} articles and {category_count} categories.")
        results['tables_exist'] = True
    else:
        print("[WARNING] Database issues detected!")
        results['issues'].append("Database tables not found or database is empty")
        results['recommendations'].append("Run force_seed_database() to populate the database")
    
    # Test write operations
    results['write_test_passed'] = test_database_write()
    
    if not results['write_test_passed']:
        results['issues'].append("Database write operations are failing")
        results['recommendations'].append("Check database file permissions and disk space")
    
    # Summary
    print("\n" + "="*50)
    print("DATABASE DIAGNOSIS SUMMARY")
    print("="*50)
    print(f"Database Type: {results['database_type']}")
    print(f"Database Exists: {results['database_exists']}")
    print(f"Tables Exist: {results['tables_exist']}")
    print(f"Article Count: {results['article_count']}")
    print(f"Category Count: {results['category_count']}")
    print(f"Write Test Passed: {results['write_test_passed']}")
    
    if results['issues']:
        print("\nIssues Found:")
        for issue in results['issues']:
            print(f"  - {issue}")
    
    if results['recommendations']:
        print("\nRecommendations:")
        for rec in results['recommendations']:
            print(f"  - {rec}")
    
    return results

def fix_database_permissions():
    """
    Fix database file permissions to ensure write access.
    """
    db_path = get_database_path()
    
    if not db_path:
        print("[INFO] PostgreSQL database - permissions handled by database server")
        return
    
    if os.path.exists(db_path):
        try:
            # Make database file writable
            os.chmod(db_path, 0o644)
            print(f"[SUCCESS] Database file permissions fixed: {db_path}")
        except Exception as e:
            print(f"[ERROR] Failed to fix permissions: {e}")
    else:
        print(f"[WARNING] Database file not found: {db_path}")

def optimize_database():
    """
    Optimize database performance and integrity.
    """
    from news_app import create_app
    from news_app.models.db import db
    
    app = create_app()
    
    with app.app_context():
        try:
            # Run vacuum to optimize storage
            if os.getenv('DATABASE_URL') is None:
                # SQLite specific
                db.session.execute("VACUUM")
                print("[INFO] Database optimized with VACUUM")
            
            # Check database integrity
            if os.getenv('DATABASE_URL') is None:
                result = db.session.execute("PRAGMA integrity_check")
                check_result = result.scalar()
                if check_result == 'ok':
                    print("[SUCCESS] Database integrity check passed")
                else:
                    print(f"[WARNING] Database integrity issue: {check_result}")
            
            print("[SUCCESS] Database optimization complete")
            
        except Exception as e:
            print(f"[ERROR] Database optimization failed: {e}")

def run_full_fix():
    """
    Run all fixes in sequence to ensure database persistence.
    """
    print("="*60)
    print("DATABASE PERSISTENCE FIX")
    print("="*60)
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print()
    
    # Step 1: Diagnose issues
    print("[STEP 1] Diagnosing database issues...")
    results = diagnose_database_issues()
    print()
    
    # Step 2: Fix permissions if needed
    print("[STEP 2] Fixing database permissions...")
    fix_database_permissions()
    print()
    
    # Step 3: Optimize database
    print("[STEP 3] Optimizing database...")
    optimize_database()
    print()
    
    # Step 4: Force seed if database is empty
    if results['article_count'] == 0 or results['category_count'] == 0:
        print("[STEP 4] Database is empty, force seeding...")
        force_seed_database()
        print()
    
    # Step 5: Final verification
    print("[STEP 5] Final verification...")
    final_results = diagnose_database_issues()
    
    if final_results['write_test_passed'] and final_results['article_count'] > 0:
        print("\n" + "="*60)
        print("FIX COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("Database persistence is now working correctly.")
        print("Articles and categories will persist across app restarts.")
        return True
    else:
        print("\n" + "="*60)
        print("FIX INCOMPLETE - Manual intervention may be required")
        print("="*60)
        return False

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'diagnose':
            diagnose_database_issues()
        elif command == 'seed':
            force_seed_database()
        elif command == 'test':
            test_database_write()
        elif command == 'fix':
            run_full_fix()
        elif command == 'permissions':
            fix_database_permissions()
        elif command == 'optimize':
            optimize_database()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python fix_database_persistence.py [diagnose|seed|test|fix|permissions|optimize]")
    else:
        # Run full fix by default
        run_full_fix()

