#!/usr/bin/env python3
"""
Database Persistence Fix for Render.com

This script diagnoses and helps fix database persistence issues.
Run this locally to test, and see INSTRUCTIONS below for Render fixes.
"""
import os
import sys

def check_database_config():
    """Check current database configuration"""
    print("=" * 60)
    print("DATABASE PERSISTENCE DIAGNOSTIC")
    print("=" * 60)
    
    # Check DATABASE_URL environment variable
    database_url = os.getenv('DATABASE_URL', '')
    
    print("\n1. DATABASE_URL Environment Variable:")
    if database_url:
        if database_url.startswith('postgres'):
            print(f"   ✅ Set: {database_url[:50]}...")
            print("   ✅ Using PostgreSQL - DATA WILL PERSIST")
        else:
            print(f"   ⚠️  Set but unexpected format: {database_url}")
    else:
        print("   ❌ NOT SET - Using SQLite (data will be lost!)")
        print("   💡 Fix: Set DATABASE_URL environment variable")
    
    print("\n2. Database Type:")
    if not database_url:
        print("   Using: SQLite (file: news.db)")
        print("   ❌ Data is EPHEMERAL - will be lost on restart/redeploy!")
    elif database_url.startswith('postgres'):
        print("   Using: PostgreSQL")
        print("   ✅ Data is PERSISTENT")
    else:
        print(f"   Unknown type from URL")
    
    print("\n3. Testing Database Connection:")
    try:
        from news_app import create_app
        from news_app.models.db import db
        from news_app.services.article_service import list_articles
        from news_app.services.category_service import list_categories
        
        app = create_app()
        with app.app_context():
            articles = list_articles()
            categories = list_categories()
            print(f"   ✅ Connection successful!")
            print(f"   📰 Articles: {len(articles)}")
            print(f"   📂 Categories: {len(categories)}")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
    
    print("\n" + "=" * 60)
    print("INSTRUCTIONS TO FIX DATABASE PERSISTENCE ON RENDER.COM")
    print("=" * 60)
    print("""
STEP 1: Create PostgreSQL Database on Render
---------------------------------------------
1. Go to https://dashboard.render.com
2. Click "New +" → "PostgreSQL"
3. Configure:
   - Name: news-db
   - Database Name: news
   - User: news
   - Plan: Free
4. Click "Create Database"
5. Wait for status to become "Available" (green)

STEP 2: Connect Database to Web Service
----------------------------------------
1. Go to your web service (news-app)
2. Click "Environment" tab
3. Under "Connections", find "news-db"
4. Click "Connect"
   - OR manually add: Key: DATABASE_URL, Value: (copy from PostgreSQL page)

STEP 3: Redeploy Your Service
------------------------------
1. Go to your web service
2. Click "Deploy" → "Deploy latest commit"
3. Wait for deployment to complete

STEP 4: Verify Persistence
--------------------------
1. Visit: https://your-app.onrender.com/api/health
2. Look for:
   - "type": "PostgreSQL" (not SQLite!)
   - "status": "connected"
   - Article and category counts > 0

STEP 5: Test Persistence
-------------------------
1. Add a new article via /admin/create_article
2. Redeploy your service (push a small change or use "Deploy")
3. Visit the site again - article should still be there!

IMPORTANT NOTES:
----------------
- Free tier PostgreSQL: Data persists but service may sleep after 15 min inactivity
- Free tier web service: Will sleep when not in use (cold starts)
- To keep awake: Upgrade to paid plan OR use health check pinger

FILES ALREADY FIXED:
---------------------
✅ render.yaml - Updated to use correct gunicorn module (app:app)
✅ news_app/controllers/api_controller.py - Enhanced health check with DB status
""")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    check_database_config()

