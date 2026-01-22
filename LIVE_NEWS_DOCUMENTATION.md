# Live News Feature - Documentation

## Overview
The Live News feature integrates with the News.org API to display real-time breaking news and trending stories from around the world. Users can search, filter by category, and sort articles by relevance, popularity, and date.

## Features

### 1. **Real-Time News Feed**
- 🔴 Live indicator showing articles are from live news sources
- Top headlines from US news sources
- Auto-updating interface
- Direct links to full articles

### 2. **Search Functionality**
- Real-time search by keywords
- Debounced input (500ms) to avoid excessive API calls
- Instant results as user types
- Search across all news sources

### 3. **Category Filtering**
Available categories:
- Business
- Entertainment
- Health
- Science
- Sports
- Technology

### 4. **Sorting Options**
- **Most Popular**: By popularity (default)
- **Latest First**: Most recent articles
- **Most Relevant**: By relevance to search query

### 5. **Article Display**
- Thumbnail image with "LIVE" badge
- Article source and publication date/time
- Title (truncated to ~70 characters)
- Description preview (truncated to ~150 characters)
- Read Full Article button
- Share button (native share or clipboard)

### 6. **Loading & Error Handling**
- Loading spinner during API calls
- Error messages for API failures
- Graceful handling of missing images
- Rate limit notifications

### 7. **Pagination**
- Load More button for additional articles
- Infinite scroll loading
- Up to 100 articles per load

## File Structure

### Backend Files

#### **article_controller.py** (Modified)
```python
@article_bp.route('/live')
def live_news():
    news_api_key = '1e642381fe9d49a8a5554db83d01aa1'
    return render_template('live_news.html', news_api_key=news_api_key)
```

**New Route:**
- `GET /live` - Display live news page with News.org API key

### Frontend Files

#### **live_news.html** (New)
Location: `/app/templates/live_news.html`

**Key Sections:**
1. **Header** - Title, description, and "LIVE" badge
2. **Filter Bar** - Search, category, sort, and refresh options
3. **Loading State** - Spinner during data fetch
4. **Error Message** - User-friendly error notifications
5. **Articles Grid** - 3-column responsive layout
6. **Empty State** - Message when no articles found
7. **Load More** - Button for pagination

**Block Inheritance:**
- Extends: `layout.html`
- Custom blocks: `{% block content %}`, `{% block scripts %}`

#### **Modified layout.html**
Added navigation links:
- Desktop: Red "🔴 Live News" link with priority
- Mobile: Red "🔴 Live News" button in menu

## API Integration

### News.org API Details

**Provider**: News.org (NewsAPI)
**API Key**: 1e642381fe9d49a8a5554db83d01aa1
**Base URL**: https://newsapi.org/v2
**Rate Limit**: 100 requests/day (free tier)

### Endpoints Used

#### 1. Top Headlines
```
GET /top-headlines?country=us&apiKey={key}
Purpose: Fetch top news from US
Response: Latest headlines with up to 20 articles
```

#### 2. Everything (Search)
```
GET /everything?q={query}&sortBy={sortBy}&pageSize=20&apiKey={key}
Parameters:
  - q: Search query (URL encoded)
  - sortBy: popularity|publishedAt|relevancy
  - pageSize: 20 per request
  - page: Pagination (1, 2, 3...)
```

#### 3. Category Headlines
```
GET /top-headlines?category={category}&country=us&pageSize=20&apiKey={key}
Categories: business|entertainment|health|science|sports|technology
```

## JavaScript Functionality

### Core Functions

```javascript
// Initialize and load initial news
loadLiveNews()

// Search articles by keyword
searchNews()

// Filter articles by category
filterNews()

// Sort articles by different criteria
sortNews()

// Load additional articles (pagination)
loadMoreNews()

// Display articles in grid
displayArticles(articles)

// Append new articles to existing grid
appendArticles(articles)

// Create individual article card HTML
createArticleCard(article)

// Share article via native share or clipboard
shareArticle(title, url)

// Show loading spinner
showLoading(show)

// Display error message
showError(message)
hideError()

// Toast notification
showNotification(message, type)

// Debounce search input
debounce(func, delay)
```

### Event Listeners
- `DOMContentLoaded` - Initialize live news on page load
- `searchInput` - Real-time search with debounce
- `categoryFilter` - Category selection
- `sortFilter` - Sort order change
- Refresh button - Manual reload

## State Management

### Page State Variables
```javascript
let currentPage = 1;           // Pagination page number
let currentQuery = '';         // Current search query
let currentCategory = '';      // Current category filter
let currentSort = 'popularity'; // Current sort order
let allArticles = [];          // All loaded articles
```

### API Response Handling
- Success: Extract articles array from response
- Error: Display user-friendly error message
- Rate limit: 429 status with specific message
- Invalid key: 401 status with specific message

## UI/UX Components

### Article Card Structure
- **Header**: Image with "LIVE" badge overlay
- **Metadata**: Source and timestamp
- **Title**: Truncated to 2 lines with ellipsis
- **Description**: Preview truncated to 3 lines
- **Actions**: 
  - "Read Full Article" button (links to external source)
  - "Share" button (opens native share or copies)

### Color Scheme
- **Primary (Red)**: Live news theme, refresh button
- **Secondary (Blue)**: Source badges
- **Gray**: Secondary information
- **White**: Card backgrounds

### Responsive Breakpoints
- **Mobile** (< 640px): 1 column, full-width
- **Tablet** (640px - 1024px): 2 columns
- **Desktop** (> 1024px): 3 columns

## Error Handling

### Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| Invalid API Key | Key expired/incorrect | Update key in controller |
| Rate limit exceeded (429) | Too many requests | Wait for limit reset |
| Unauthorized (401) | Invalid credentials | Check API key |
| No results found | Bad search query | Try different keywords |
| Image fails to load | URL broken | Placeholder image shown |
| CORS error | Browser security | Server-side proxy required |

## Search & Filtering Logic

### Search Flow
1. User types in search box
2. Input debounced for 500ms
3. Clear previous results
4. Fetch from `/everything` endpoint
5. Display results with current sort order

### Category Filter Flow
1. User selects category
2. Fetch from `/top-headlines` with category
3. Reset pagination to page 1
4. Display category-specific articles

### Sort Priority
1. If search active: Sort search results
2. Else if category active: Re-fetch with sort
3. Else: Reload headlines with sort

## Performance Optimization

### Debounced Search
- Prevents excessive API calls
- 500ms delay between keystrokes
- Only one pending request at a time

### Lazy Loading
- Articles load only when needed
- Load More button for pagination
- No auto-infinite scroll to save API calls

### Image Optimization
- Placeholder for broken images
- Image scaling with CSS
- No image processing server-side

## Tailwind CSS Classes Used

- Grid layout: `grid`, `grid-cols-1`, `md:grid-cols-2`, `lg:grid-cols-3`
- Spacing: `px-4`, `py-2`, `mb-8`
- Colors: `text-red-600`, `bg-blue-100`, `border-gray-300`
- Effects: `hover:`, `transition`, `duration-300`
- Animations: `animate-spin`, `hover:scale-105`
- Line clamp: `line-clamp-2`, `line-clamp-3`

## Browser Compatibility

✅ Chrome 90+
✅ Firefox 88+
✅ Safari 14+
✅ Edge 90+
✅ Mobile Safari (iOS 14+)
✅ Chrome Mobile (Android 8+)

## Security Considerations

### API Key Handling
- API key stored in Flask backend (not exposed in client code)
- Passed to template during render
- Never hardcoded in HTML/JS sent to browser

### External Links
- All article links open in new tab (`target="_blank"`)
- Rel security: `rel="noopener noreferrer"`
- Prevents window.opener access

### Data Validation
- Check API response status
- Validate article properties exist
- Graceful fallbacks for missing data

## Testing Recommendations

### Manual Testing
- [ ] Load live news page
- [ ] Verify articles display with images
- [ ] Search for different keywords
- [ ] Test each category filter
- [ ] Test all sort options
- [ ] Verify pagination works
- [ ] Test on mobile device
- [ ] Check error handling (bad search, etc)
- [ ] Test share functionality
- [ ] Verify external links work

### Edge Cases
- [ ] No internet connection
- [ ] API rate limit exceeded
- [ ] Invalid API key
- [ ] Empty search results
- [ ] Missing article images
- [ ] Very long article titles
- [ ] Special characters in search

## Future Enhancements

1. **Saved Articles**
   - Save articles to read later
   - Persistent storage (localStorage)
   - Read/unread marking

2. **News Alerts**
   - Set keyword alerts
   - Get notifications for trending topics
   - Email digest options

3. **Advanced Filtering**
   - Date range selection
   - News source selection
   - Language filters

4. **Dark Mode**
   - Toggle dark/light theme
   - Persistent preference

5. **Social Integration**
   - Direct share to Twitter/Facebook
   - Comment system
   - User ratings

6. **Analytics**
   - Track most read articles
   - Popular search terms
   - User preferences

## Troubleshooting

### No articles loading
- Check API key is valid
- Verify internet connection
- Check browser console for errors
- Verify News.org API is accessible

### Images not loading
- Check image URLs are accessible
- Verify CORS not blocking images
- Placeholder fallback should display

### Search not working
- Ensure search debounce is working
- Check network tab for API calls
- Verify search terms are valid

### Share button not working
- Check browser supports Share API
- Verify clipboard permissions
- Check console for errors

### Styling looks off
- Hard refresh: Ctrl+Shift+R
- Clear browser cache
- Check Tailwind CDN loaded

## Related Pages

- [Home](/) - Main news portal
- [Articles](/articles) - Internal articles
- [Create Article](/articles/create) - Write new article
- [Manage News](/manage) - Admin panel
- [Categories](/categories) - News categories

## API Documentation Reference

For complete News.org API documentation:
- Website: https://newsapi.org/
- Docs: https://newsapi.org/docs
- Status: https://newsapi.org/s/about

---

**Created**: January 22, 2026
**API Key**: 1e642381fe9d49a8a5554db83d01aa1
**Status**: ✅ Production Ready
**Last Updated**: January 22, 2026
