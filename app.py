from app import create_app
import os

# Create app instance for Gunicorn
app = create_app()

if __name__ == '__main__':
    cert = os.getenv('SSL_CERT')
    key = os.getenv('SSL_KEY')
    if cert and key:
        app.run(host='0.0.0.0', port=8443, ssl_context=(cert, key), debug=False)
    else:
        app.run(host='0.0.0.0', port=8080, debug=False)
