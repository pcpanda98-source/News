# NewsAPI.org Integration Guide

## ✅ Setup Complete!

Your News application is now integrated with **NewsAPI.org** using your API key.

### API Key
- **Key**: `7ee335fefcc3490982cb790ed9f85c8a`
- **Status**: ✅ Active and Working

---

## 📚 Available Endpoints

### 1. **Top Headlines**
Get top headlines from NewsAPI.org

**Endpoint**: `/api/live`

**Query Parameters**:
- `country` (optional): Country code (e.g., `us`, `gb`, `fr`) - Default: `us`
- `category` (optional): News category - Options: `business`, `entertainment`, `health`, `science`, `sports`, `technology`
- `page` (optional): Page number - Default: `1`
- `pageSize` (optional): Number of articles per page - Default: `10` (Max: `100`)

**Example**:
```bash
curl "http://localhost:8080/api/live?country=us&category=technology&pageSize=5"
```

**Response**:
```json
{
  "status": "ok",
  "totalResults": 33,
  "articles": [
    {
      "title": "Article Title",
      "description": "Article description...",
      "url": "https://...",
      "urlToImage": "https://...",
      "source": {"name": "Source Name"},
      "publishedAt": "2026-01-27T10:00:00Z",
      "author": "Author Name",
      "content": "Full article content..."
    }
  ]
}
```

---

### 2. **Search News**
Search for articles by keyword

**Endpoint**: `/api/search`

**Query Parameters**:
- `q` (required): Search query keyword
- `from` (optional): Start date (YYYY-MM-DD format)
- `to` (optional): End date (YYYY-MM-DD format)
- `sortBy` (optional): Sort results - Options: `publishedAt`, `relevancy`, `popularity` - Default: `publishedAt`
- `page` (optional): Page number - Default: `1`
- `pageSize` (optional): Articles per page - Default: `10`

**Example**:
```bash
curl "http://localhost:8080/api/search?q=artificial%20intelligence&sortBy=relevancy&pageSize=10"
```

---

### 3. **Get News Sources**
Get available news sources from NewsAPI.org

**Endpoint**: `/api/sources`

**Response**:
```json
{
  "status": "ok",
  "sources": [
    {
      "id": "bbc-news",
      "name": "BBC News",
      "description": "Use BBC News for up-to-the-minute news...",
      "url": "http://www.bbc.co.uk/news",
      "category": "general",
      "language": "en",
      "country": "gb"
    }
  ]
}
```

---

### 4. **Health Check**
Check if the API is running

**Endpoint**: `/api/health`

**Response**:
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

---

## 🚀 Quick Start Examples

### Python Examples
```python
from app.services.news_service import top_headlines, search_news

# Get top US headlines
headlines = top_headlines(country='us', category='technology')

# Search for articles
results = search_news('Python programming', page_size=5)

# Get all results with pagination
results = search_news('cryptocurrency', page=2, page_size=20)
```

### Using curl
```bash
# Get top headlines
curl "http://localhost:8080/api/live?country=us&pageSize=5"

# Search for news
curl "http://localhost:8080/api/search?q=machine%20learning"

# Get available sources
curl "http://localhost:8080/api/sources"
```

---

## ⚙️ Configuration

The API key is stored in `.env` file:
```
NEWS_API_KEY=7ee335fefcc3490982cb790ed9f85c8a
```

To change it, edit `.env` and restart the application.

---

## 📊 Supported Countries

```
ae, ar, at, au, be, bg, br, by, ca, ch, cn, co, cu, cz, de, eg, fr, gb, gr, 
hk, hu, id, ie, il, in, it, jp, kr, kz, lb, lt, lv, ma, mx, my, ng, nl, no, 
nz, ph, pl, pt, ro, rs, ru, sa, se, sg, si, sk, th, tr, tw, ua, us, ve, za, zw
```

---

## 📁 Key Files Modified

- `app/services/news_service.py` - NewsAPI integration service
- `app/controllers/api_controller.py` - API endpoints
- `.env` - Configuration file with API key

---

## ✨ Features

✅ Real-time news from NewsAPI.org  
✅ Filter by country and category  
✅ Search functionality  
✅ Pagination support  
✅ Error handling  
✅ Multiple response formats  
✅ Source information  

---

## 🔗 NewsAPI Documentation

Visit [newsapi.org](https://newsapi.org) for:
- API documentation
- Rate limits (free plan: 100 requests/day)
- Additional features
- API status

---

## 🆘 Troubleshooting

**Getting "401 Unauthorized"?**
- Check if your API key is correct in `.env`
- Verify the key is active at newsapi.org

**Getting "429 Too Many Requests"?**
- You've exceeded the daily limit for your free API key
- Upgrade to a paid plan or wait until the next day

**Getting empty results?**
- Verify the country code is valid
- Try different search terms
- Check if the category is spelled correctly

---

**Status**: ✅ Ready to use!
**Last Updated**: January 27, 2026
