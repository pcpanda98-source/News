# News Management App

Simple news management system (Flask backend, vanilla JS frontend). Features:
- Live news (uses NewsAPI with provided key)
- Create/View/Edit/Delete internal articles
- Category management
- Admin dashboard

Quick start (dev):

1. Create a virtualenv and install:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. (Optional) Configure environment variables in `.env`:

```
DATABASE_URL=sqlite:///news.db
NEWS_API_KEY=pub_b6ea65c0579b42b5a8f61d11f2eac14f
SSL_CERT=/path/to/cert.pem
SSL_KEY=/path/to/key.pem
```

3. Run app:

```bash
python -m app.main
```

If you set `SSL_CERT` and `SSL_KEY` the app will run on port `8443` with HTTPS; otherwise it runs HTTP on `8080`.

To generate a local self-signed cert for dev:

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/CN=localhost"
```
# News