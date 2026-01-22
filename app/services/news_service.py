import requests
import os

API_KEY = os.getenv('NEWS_API_KEY', 'pub_b6ea65c0579b42b5a8f61d11f2eac14f')
BASE = 'https://newsdata.io/api/1/news'

def top_headlines(country='us', category=None):
    params = {'apikey': API_KEY}
    if country:
        params['country'] = country
    if category:
        params['category'] = category
    r = requests.get(f'{BASE}', params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    # Transform NewsData.io response to match expected format
    if data.get('status') == 'success':
        return {
            'articles': [
                {
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'url': article.get('link', ''),
                    'urlToImage': article.get('image_url', ''),
                    'source': {'name': article.get('source_id', 'Unknown')},
                    'publishedAt': article.get('pubDate', '')
                }
                for article in data.get('results', [])
            ]
        }
    return {'articles': []}
