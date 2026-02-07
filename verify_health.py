"""
Database Health Verification Script

This script provides a quick health check for the database system,
verifying that data persistence is working correctly.
"""

import os
import sys

def check_database_health():
    """
    Perform a comprehensive health check on the database.
    Returns: (is_healthy, details_dict)
    """
    details = {
        'database_type': 'unknown',
        'database_exists': False,
        'article_count': 0,
        'category_count': 0,
        'can_write': False,
        'issues': []
    }
    
    # Check database type
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        details['database_type'] = 'postgresql'
    else:
        details['database_type'] = 'sqlite'
        # Check SQLite file exists
        db_path = os.path.abspath('news.db')
        details['database_exists'] = os.path.exists(db_path)
        if not details['database_exists']:
            details['issues'].append('SQLite database file not found')
    
    # Try to connect and query
    try:
        from news_app import create_app
        from news_app.models.db import db
        from news_app.services.article_service import list_articles
        from news_app.services.category_service import list_categories
        
        app = create_app()
        
        with app.app_context():
            # Test connection
            from sqlalchemy import text
            db.session.execute(text("SELECT 1"))
            
            # Get counts
            articles = list_articles()
            categories = list_categories()
            
            details['article_count'] = len(articles)
            details['category_count'] = len(categories)
            details['database_exists'] = True
            
            # Test write capability
            from news_app.services.article_service import create_article, delete_article
            
            initial_count = len(articles)
            test_article = create_article(
                f"Health Check Test {os.getpid()}",
                "Testing database write capability",
                None,
                "Health Check"
            )
            
            if test_article and test_article.id:
                # Verify it was saved
                new_count = len(list_articles())
                details['can_write'] = new_count > initial_count
                
                # Clean up
                delete_article(test_article.id)
            else:
                details['issues'].append('Could not create test article')
            
    except Exception as e:
        details['issues'].append(f'Database connection failed: {e}')
        return False, details
    
    # Determine health status
    is_healthy = (
        details['database_exists'] and
        details['can_write'] and
        len(details['issues']) == 0
    )
    
    return is_healthy, details

def print_health_report():
    """Print a formatted health report"""
    print("="*60)
    print("DATABASE HEALTH REPORT")
    print("="*60)
    
    is_healthy, details = check_database_health()
    
    print(f"Database Type: {details['database_type']}")
    print(f"Database Exists: {details['database_exists']}")
    print(f"Article Count: {details['article_count']}")
    print(f"Category Count: {details['category_count']}")
    print(f"Can Write: {details['can_write']}")
    
    if details['issues']:
        print("\nIssues Found:")
        for issue in details['issues']:
            print(f"  - {issue}")
    
    print("\n" + "="*60)
    if is_healthy:
        print("STATUS: ✓ HEALTHY")
        print("="*60)
        print("✓ Database is working correctly")
        print("✓ Data persistence is functional")
        print("✓ New articles and categories can be saved")
    else:
        print("STATUS: ✗ UNHEALTHY")
        print("="*60)
        print("⚠️  Database has issues that need attention")
        print("⚠️  New articles/categories may not be saved")
    
    return is_healthy

def suggest_fix():
    """Provide suggestions for fixing database issues"""
    print("\n" + "="*60)
    print("SUGGESTED FIXES")
    print("="*60)
    
    print("1. If database file doesn't exist:")
    print("   Run: python fix_database_persistence.py seed")
    
    print("\n2. If write operations fail:")
    print("   - Check file permissions: chmod 644 news.db")
    print("   - Ensure disk has available space")
    print("   - Run: python fix_database_persistence.py fix")
    
    print("\n3. For production (Render.com):")
    print("   - Verify DATABASE_URL environment variable is set")
    print("   - Check PostgreSQL connection in logs")
    print("   - Run: python test_database.py")
    
    print("\n4. To reset everything:")
    print("   Run: python fix_database_persistence.py fix")

if __name__ == '__main__':
    print("\n")
    is_healthy = print_health_report()
    
    if not is_healthy:
        suggest_fix()
    
    sys.exit(0 if is_healthy else 1)

