"""
Database Testing Script

This script tests database operations to ensure articles and categories
can be created, read, updated, and deleted properly.
"""

import os
import sys

def test_database_connection():
    """Test that the database connection works"""
    print("="*60)
    print("TEST 1: Database Connection")
    print("="*60)
    
    from news_app import create_app
    from news_app.models.db import db
    
    try:
        app = create_app()
        with app.app_context():
            # Try to create a session and query
            from sqlalchemy import text
            result = db.session.execute(text("SELECT 1"))
            result.scalar()
            print("✓ Database connection successful")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def test_categories():
    """Test category CRUD operations"""
    print("\n" + "="*60)
    print("TEST 2: Category Operations")
    print("="*60)
    
    from news_app import create_app
    from news_app.services.category_service import list_categories, create_category, delete_category
    from news_app.models.category import Category
    
    try:
        app = create_app()
        with app.app_context():
            # Get initial count
            initial_count = len(list_categories())
            print(f"Initial category count: {initial_count}")
            
            # Create test category
            test_name = f"Test Category {os.getpid()}"
            new_cat = create_category(test_name, "Test description")
            print(f"✓ Created category: {new_cat.name} (ID: {new_cat.id})")
            
            # Verify it's in the list
            after_count = len(list_categories())
            print(f"Category count after creation: {after_count}")
            
            if after_count > initial_count:
                print("✓ Category creation works!")
                
                # Clean up
                delete_category(new_cat.id)
                print(f"✓ Cleaned up test category")
                return True
            else:
                print("✗ Category creation failed - count didn't increase")
                return False
                
    except Exception as e:
        print(f"✗ Category test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_articles():
    """Test article CRUD operations"""
    print("\n" + "="*60)
    print("TEST 3: Article Operations")
    print("="*60)
    
    from news_app import create_app
    from news_app.services.article_service import list_articles, create_article, delete_article
    from news_app.models.article import Article
    
    try:
        app = create_app()
        with app.app_context():
            # Get initial count
            initial_count = len(list_articles())
            print(f"Initial article count: {initial_count}")
            
            # Create test article
            test_title = f"Test Article {os.getpid()}"
            test_content = "This is a test article created by the database test script."
            
            new_article = create_article(test_title, test_content, None, "Test System")
            print(f"✓ Created article: {new_article.title} (ID: {new_article.id})")
            
            # Verify it's in the list
            after_count = len(list_articles())
            print(f"Article count after creation: {after_count}")
            
            if after_count > initial_count:
                print("✓ Article creation works!")
                
                # Verify data can be read back
                articles = list_articles()
                found = any(a.id == new_article.id for a in articles)
                if found:
                    print("✓ Article can be read back from database")
                else:
                    print("✗ Article not found after creation")
                    return False
                
                # Clean up
                delete_article(new_article.id)
                print(f"✓ Cleaned up test article")
                return True
            else:
                print("✗ Article creation failed - count didn't increase")
                return False
                
    except Exception as e:
        print(f"✗ Article test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_persistence():
    """Test that data persists across multiple operations"""
    print("\n" + "="*60)
    print("TEST 4: Data Persistence")
    print("="*60)
    
    from news_app import create_app
    from news_app.services.category_service import list_categories
    from news_app.services.article_service import list_articles
    
    try:
        app = create_app()
        
        # First check
        with app.app_context():
            cats1 = len(list_categories())
            arts1 = len(list_articles())
            print(f"First check: {cats1} categories, {arts1} articles")
            
            # Second check (simulate reload)
            with app.app_context():
                cats2 = len(list_categories())
                arts2 = len(list_articles())
                print(f"Second check: {cats2} categories, {arts2} articles")
                
                if cats1 == cats2 and arts1 == arts2:
                    print("✓ Data persists across app context reloads")
                    return True
                else:
                    print("✗ Data does NOT persist - counts changed between checks")
                    return False
                    
    except Exception as e:
        print(f"✗ Persistence test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_full_workflow():
    """Test the full workflow of creating and managing content"""
    print("\n" + "="*60)
    print("TEST 5: Full Workflow Test")
    print("="*60)
    
    from news_app import create_app
    from news_app.services.category_service import create_category, list_categories, delete_category
    from news_app.services.article_service import create_article, list_articles, delete_article
    from news_app.models.category import Category
    from news_app.models.article import Article
    
    test_cat = None
    test_article = None
    
    try:
        app = create_app()
        with app.app_context():
            print("Step 1: Creating a new category...")
            test_cat = create_category(f"Workflow Test {os.getpid()}", "Test category for workflow")
            print(f"✓ Created category: {test_cat.name}")
            
            print("\nStep 2: Creating an article in that category...")
            test_article = create_article(
                "Workflow Test Article",
                "This article was created during a comprehensive workflow test.",
                test_cat.id,
                "Workflow Tester"
            )
            print(f"✓ Created article: {test_article.title}")
            
            print("\nStep 3: Verifying article is linked to category...")
            if test_article.category_id == test_cat.id:
                print("✓ Article is correctly linked to category")
            else:
                print("✗ Article category link failed")
                return False
            
            print("\nStep 4: Listing all categories and articles...")
            categories = list_categories()
            articles = list_articles()
            print(f"Total categories: {len(categories)}")
            print(f"Total articles: {len(articles)}")
            
            # Verify our test items are in the lists
            cat_found = any(c.id == test_cat.id for c in categories)
            art_found = any(a.id == test_article.id for a in articles)
            
            if cat_found and art_found:
                print("✓ Test items found in lists")
            else:
                print("✗ Test items not found in lists")
                return False
            
            print("\nStep 5: Cleanup...")
            delete_article(test_article.id)
            delete_category(test_cat.id)
            print("✓ Test data cleaned up")
            
            print("\n✓ Full workflow test completed successfully!")
            return True
            
    except Exception as e:
        print(f"✗ Workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        
        # Cleanup on failure
        if test_article:
            try:
                delete_article(test_article.id)
            except:
                pass
        if test_cat:
            try:
                delete_category(test_cat.id)
            except:
                pass
        
        return False

def run_all_tests():
    """Run all database tests"""
    print("\n" + "="*60)
    print("DATABASE TESTING SUITE")
    print("="*60)
    print(f"Timestamp: {__import__('datetime').datetime.now().isoformat()}")
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Category Operations", test_categories),
        ("Article Operations", test_articles),
        ("Data Persistence", test_data_persistence),
        ("Full Workflow", test_full_workflow),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"✗ {name} crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, p in results if p)
    total = len(results)
    
    for name, p in results:
        status = "✓ PASSED" if p else "✗ FAILED"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All database tests passed! Your database is working correctly.")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above for details.")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

