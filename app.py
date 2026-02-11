from news_app import create_app
import os

# Create app instance for Gunicorn
app = create_app()

# Performance: Add cache control headers for static assets
@app.after_request
def add_cache_headers(response):
    """Add caching headers for better performance"""
    # Cache CSS and JS files for 1 week
    if request.path.endswith('.css') or request.path.endswith('.js'):
        response.headers['Cache-Control'] = 'public, max-age=604800, immutable'
    # Cache static images for 1 month
    elif '/static/uploads/' in request.path or '/static/images/' in request.path:
        response.headers['Cache-Control'] = 'public, max-age=2592000'
    # Cache static files
    elif request.path.startswith('/static'):
        response.headers['Cache-Control'] = 'public, max-age=3600'
    # Don't cache HTML responses
    elif request.path.endswith('.html') or request.is_xhr:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

# Import Flask modules for caching (needs to be after app creation)
from flask import request

if __name__ == '__main__':
    cert = os.getenv('SSL_CERT')
    key = os.getenv('SSL_KEY')
    if cert and key:
        app.run(host='0.0.0.0', port=8443, ssl_context=(cert, key), debug=False)
    else:
        app.run(host='0.0.0.0', port=8080, debug=False)
