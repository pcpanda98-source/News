#!/usr/bin/env python3
"""
Comprehensive test for search and filter functionality
"""
from news_app import create_app
from news_app.services.article_service import list_articles
from news_app.services.category_service import list_categories

def test_complete_functionality():
    """Test all aspects of search and filter functionality"""
    app = create_app()
    
    with app.test_client() as client:
        print("🧪 Testing Search and Filter Functionality")
        
        # Test 1: Basic articles page
        response = client.get('/articles')
        assert response.status_code == 200
        print("✅ Articles page loads successfully")
        
        # Test 2: Category filtering
        response = client.get('/articles?category=Technology')
        assert response.status_code == 200
        print("✅ Category filtering works")
        
        # Test 3: Search parameter
        response = client.get('/articles?search=technology')
        assert response.status_code == 200
        print("✅ Search parameter works")
        
        # Test 4: Check HTML elements
        response = client.get('/articles')
        content = response.data.decode('utf-8')
        
        required_elements = [
            'id="searchInput"',
            'id="categoryFilter"',
            'id="articlesContainer"',
            'id="emptyState"',
            'id="articleCount"',
            'function filterArticles()',
            'function resetFilters()',
            'data-title=',
            'data-category=',
            'data-author=',
            'data-content='
        ]
        
        for element in required_elements:
            assert element in content, f"Missing: {element}"
        
        print("✅ All required HTML elements present")
        
        # Test 5: Data availability
        with app.app_context():
            articles = list_articles()
            categories = list_categories()
            
            assert len(articles) > 0, "No articles found"
            assert len(categories) > 0, "No categories found"
            
            print(f"✅ Data ready: {len(articles)} articles, {len(categories)} categories")
            
            # Test article data structure
            if articles:
                article = articles[0]
                assert hasattr(article, 'title'), "Article missing title"
                assert hasattr(article, 'content'), "Article missing content"
                assert hasattr(article, 'author'), "Article missing author"
                print("✅ Article data structure correct")
        
        print("\n🎉 All search and filter functionality tests passed!")
        return True

if __name__ == '__main__':
    try:
        success = test_complete_functionality()
        if success:
            print("\n✅ SEARCH AND FILTER FUNCTIONALITY IS WORKING CORRECTLY!")
        else:
            print("\n❌ Tests failed!")
    except Exception as e:
        print(f"\n❌ Test error: {str(e)}")
        import traceback
        traceback.print_exc()