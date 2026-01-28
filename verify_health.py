#!/usr/bin/env python3
"""
Health Check Script - Verify Application Integrity
Tests for critical errors and structural issues
"""

import sys
from pathlib import Path

def check_imports():
    """Verify no circular imports or import errors"""
    print("\n" + "="*60)
    print("1. CHECKING IMPORTS & CIRCULAR DEPENDENCIES")
    print("="*60)
    try:
        from app import create_app
        from app.models.article import Article
        from app.models.category import Category
        from app.models.db import db
        print("✅ All imports successful - no circular dependencies")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def check_models():
    """Verify no duplicate model definitions"""
    print("\n" + "="*60)
    print("2. CHECKING MODEL DEFINITIONS")
    print("="*60)
    try:
        from app.models.article import Article
        from app.models.category import Category
        
        # Check Article model
        article_module = Article.__module__
        print(f"✅ Article model location: {article_module}")
        if article_module != "app.models.article":
            print(f"⚠️  Warning: Article model imported from unexpected location")
            return False
        
        # Check Category model
        category_module = Category.__module__
        print(f"✅ Category model location: {category_module}")
        if category_module != "app.models.category":
            print(f"⚠️  Warning: Category model imported from unexpected location")
            return False
        
        # Verify model has required methods
        article_methods = [m for m in dir(Article) if not m.startswith('_')]
        if 'to_dict' not in article_methods:
            print("❌ Article model missing to_dict() method")
            return False
        
        print("✅ Model definitions verified - no duplicates")
        return True
    except Exception as e:
        print(f"❌ Model check error: {e}")
        return False

def check_routes():
    """Verify route conflicts are resolved"""
    print("\n" + "="*60)
    print("3. CHECKING ROUTES FOR CONFLICTS")
    print("="*60)
    try:
        from app import create_app
        app = create_app()
        
        routes = {}
        for rule in app.url_map.iter_rules():
            if rule.rule.startswith('/static') or rule.rule == '/':
                continue
            
            path = rule.rule
            method = ','.join(rule.methods - {'HEAD', 'OPTIONS'})
            
            if path not in routes:
                routes[path] = []
            routes[path].append(method)
        
        # Check for /live route conflict
        live_routes = [r for r in routes if '/live' in r]
        print(f"\n  Live routes found:")
        for route in sorted(live_routes):
            methods = routes[route]
            print(f"    ✅ {route} [{','.join(methods)}]")
        
        # Verify specific routes
        if '/live' in routes:
            print(f"\n  ❌ OLD ROUTE DETECTED: /live should be removed")
            return False
        
        if '/live-feed' not in routes:
            print(f"\n  ❌ EXPECTED ROUTE MISSING: /live-feed should exist")
            return False
        
        if '/api/live' not in routes:
            print(f"\n  ❌ EXPECTED ROUTE MISSING: /api/live should exist")
            return False
        
        print(f"\n✅ No route conflicts - all live routes properly separated")
        return True
    except Exception as e:
        print(f"❌ Route check error: {e}")
        return False

def check_database():
    """Verify database configuration and persistence"""
    print("\n" + "="*60)
    print("4. CHECKING DATABASE CONFIGURATION")
    print("="*60)
    try:
        from app import create_app
        app = create_app()
        
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        print(f"✅ Database URI: {db_uri}")
        
        # Verify it's using SQLite
        if 'sqlite' not in db_uri:
            print(f"⚠️  Warning: Expected SQLite database")
            return False
        
        # Verify single database file
        if 'news.db' not in db_uri:
            print(f"⚠️  Warning: Expected database file named 'news.db'")
            return False
        
        print("✅ Database configuration verified")
        return True
    except Exception as e:
        print(f"❌ Database check error: {e}")
        return False

def check_app_structure():
    """Verify app/__init__.py structure is correct"""
    print("\n" + "="*60)
    print("5. CHECKING APPLICATION STRUCTURE")
    print("="*60)
    try:
        init_file = Path(__file__).parent / "app" / "__init__.py"
        content = init_file.read_text()
        
        # Check that it's clean (no model definitions)
        if "class Article" in content or "class Category" in content:
            print("❌ Models should not be defined in app/__init__.py")
            return False
        
        # Check for create_app function
        if "def create_app" not in content:
            print("❌ create_app() function not found")
            return False
        
        # Check for proper imports
        if "from app.models.db import db" not in content:
            print("❌ Database import not found")
            return False
        
        print("✅ app/__init__.py is properly structured")
        print("   - No model definitions (models in separate files)")
        print("   - Contains create_app() factory function")
        print("   - Proper imports")
        return True
    except Exception as e:
        print(f"❌ Structure check error: {e}")
        return False

def main():
    """Run all health checks"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "NEWS APPLICATION HEALTH CHECK" + " "*13 + "║")
    print("╚" + "="*58 + "╝")
    
    checks = [
        ("Imports", check_imports),
        ("Models", check_models),
        ("Routes", check_routes),
        ("Database", check_database),
        ("Structure", check_app_structure),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Unexpected error in {name}: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {name}")
    
    print(f"\nResult: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✅ APPLICATION IS HEALTHY - NO CRITICAL ERRORS")
        print("="*60)
        return 0
    else:
        print("\n❌ APPLICATION HAS ISSUES - PLEASE REVIEW ABOVE")
        print("="*60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
