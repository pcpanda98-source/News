import requests
import os
from datetime import datetime, timedelta

API_KEY = os.getenv('NEWS_API_KEY', '7ee335fefcc3490982cb790ed9f85c8a')
BASE_URL = 'https://newsapi.org/v2'

def _transform_article(article):
    """Transform NewsAPI article to standard format"""
    return {
        'title': article.get('title', ''),
        'description': article.get('description', ''),
        'url': article.get('url', ''),
        'urlToImage': article.get('urlToImage', ''),
        'source': {'name': article.get('source', {}).get('name', 'Unknown')},
        'publishedAt': article.get('publishedAt', ''),
        'author': article.get('author', 'Unknown'),
        'content': article.get('content', '')
    }

def top_headlines(country='us', category=None, page=1, page_size=10):
    """Fetch top headlines from NewsAPI"""
    params = {
        'apiKey': API_KEY,
        'pageSize': page_size,
        'page': page
    }
    if country:
        params['country'] = country
    if category:
        params['category'] = category
    
    try:
        r = requests.get(f'{BASE_URL}/top-headlines', params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        if data.get('status') == 'ok':
            return {
                'status': 'ok',
                'totalResults': data.get('totalResults', 0),
                'articles': [_transform_article(article) for article in data.get('articles', [])]
            }
        return {'status': 'error', 'message': data.get('message', 'Unknown error'), 'articles': []}
    except requests.exceptions.RequestException as e:
        return {'status': 'error', 'message': str(e), 'articles': []}

def search_news(query, from_date=None, to_date=None, sort_by='publishedAt', page=1, page_size=10):
    """Search for news articles by keyword"""
    params = {
        'apiKey': API_KEY,
        'q': query,
        'pageSize': page_size,
        'page': page,
        'sortBy': sort_by
    }
    
    if from_date:
        params['from'] = from_date
    if to_date:
        params['to'] = to_date
    
    try:
        r = requests.get(f'{BASE_URL}/everything', params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        if data.get('status') == 'ok':
            return {
                'status': 'ok',
                'totalResults': data.get('totalResults', 0),
                'articles': [_transform_article(article) for article in data.get('articles', [])]
            }
        return {'status': 'error', 'message': data.get('message', 'Unknown error'), 'articles': []}
    except requests.exceptions.RequestException as e:
        return {'status': 'error', 'message': str(e), 'articles': []}

def get_sources():
    """Get available news sources"""
    params = {'apiKey': API_KEY}
    
    try:
        r = requests.get(f'{BASE_URL}/sources', params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        if data.get('status') == 'ok':
            return {
                'status': 'ok',
                'sources': data.get('sources', [])
            }
        return {'status': 'error', 'message': data.get('message', 'Unknown error'), 'sources': []}
    except requests.exceptions.RequestException as e:
        return {'status': 'error', 'message': str(e), 'sources': []}

