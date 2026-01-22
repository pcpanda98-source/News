# Live News - Quick Reference

## 🔴 Access Live News

| Method | Path |
|--------|------|
| Navigation (Desktop) | Click red "🔴 Live News" button in header |
| Navigation (Mobile) | Hamburger menu → "🔴 Live News" |
| Direct URL | `http://127.0.0.1:8080/live` |

## 🎯 What You Can Do

### Search News
1. Type keywords in search box
2. Results update in real-time (500ms delay)
3. Click "Read Full Article" to view on news source

### Filter by Category
1. Select category from dropdown
2. Options: Business, Entertainment, Health, Science, Sports, Technology
3. Select blank option to show all categories

### Sort Articles
1. Choose sort method: Most Popular, Latest First, Most Relevant
2. Articles reorganize automatically
3. Works with search and category filters

### Refresh News
- Click 🔄 Refresh button to reload latest headlines
- Useful to get most recent breaking news

### Load More Articles
- Click "Load More Articles" button at bottom
- Adds next batch of articles to page
- Up to 100 articles can be loaded

### Read Articles
1. Click "Read Full Article" button on any card
2. Opens article in new tab on original source
3. Click "Share" to share article

## 📰 Article Card Information

```
[LIVE IMAGE BADGE]
Source | Publication Date/Time
Article Title (truncated)
Description Preview (truncated)
[Read Full Article] [Share]
```

## 🔍 Search Tips

| Query | Result |
|-------|--------|
| "COVID-19" | Articles about COVID-19 |
| "Apple" | News about Apple Inc |
| "Climate" | Climate change articles |
| "Elections" | Election news |
| "Tech startup" | Multi-word searches |

## 📊 Available Categories

- 💼 Business - Markets, companies, finance
- 🎬 Entertainment - Movies, music, celebrities
- 🏥 Health - Medical, health, wellness
- 🔬 Science - Research, discoveries, space
- ⚽ Sports - Games, athletes, competitions
- 💻 Technology - Tech news, gadgets, software

## 🎨 UI Features

| Element | Purpose |
|---------|---------|
| Red 🔴 Badge | Indicates live news source |
| Blue Source Badge | Shows news organization |
| Timestamp | When article was published |
| Image | Article thumbnail |
| Title | Main headline |
| Description | Article preview/summary |

## ⚙️ Sort Options

1. **Most Popular** (default) - Articles ranked by engagement/views
2. **Latest First** - Newest articles appear first
3. **Most Relevant** - Best match to your search query

## 💾 Storage & Data

- Articles stored in browser cache during session
- Load More button adds articles without clearing previous
- Page refresh resets to top headlines
- Search results persist until category change

## 🚀 Performance

| Action | Speed |
|--------|-------|
| Initial load | ~2-3 seconds |
| Search (after debounce) | ~1-2 seconds |
| Category filter | ~1-2 seconds |
| Sort change | Instant |
| Load more | ~2-3 seconds |

## 📱 Mobile Features

- Responsive design: 1 column on mobile
- Touch-friendly buttons
- Full width layout
- Swipe-friendly cards
- Hamburger menu navigation

## 🔗 Integration with Other Pages

| Page | Link |
|------|------|
| Home | Go to home to see featured articles |
| Articles | View internal articles |
| Create Article | Write your own article |
| Manage News | Admin panel for articles |
| Categories | Browse news by category |

## ⚠️ Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| No articles show | Wait 2-3 seconds for load, refresh page |
| Images don't load | Placeholder appears, check internet |
| Search no results | Try different keywords, check spelling |
| Share not working | Use clipboard fallback or try again |
| Styling looks broken | Hard refresh (Ctrl+Shift+R) |

## 🎯 Best Practices

✅ Use specific keywords for targeted searches
✅ Combine category filter with search for best results
✅ Sort by "Latest First" for breaking news
✅ Use "Load More" instead of refreshing to see new articles
✅ Open articles in new tab to keep news page open

❌ Don't search for single letters (returns too many results)
❌ Don't load too many pages (API rate limits)
❌ Don't refresh page repeatedly (use Refresh button instead)

## 🔑 API Information

| Detail | Value |
|--------|-------|
| Provider | News.org (NewsAPI) |
| API Key | 1e642381fe9d49a8a5554db83d01aa1 |
| Free Tier | 100 requests/day |
| Rate Limit | Requests per day |

## 📊 What You See

- **Article Source**: Who published the article
- **Timestamp**: When article was published (date + time)
- **Title**: Main headline (truncated to ~70 chars)
- **Preview**: First ~150 characters of description
- **Image**: Thumbnail from article
- **LIVE Badge**: Indicates real-time news source

## 🎮 Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Focus search | Click search box or Tab |
| Submit search | Press Enter |
| Navigate | Tab through filters |
| Close dropdown | Press Escape |

## 📞 Support

### Page Not Loading?
1. Check internet connection
2. Refresh page
3. Clear browser cache
4. Try different browser

### No Results?
1. Try different search term
2. Clear search and try category
3. Check search spelling

### Share Not Working?
1. Refresh page
2. Try share button again
3. Use clipboard fallback

## 📱 Mobile Tips

- Tap search box to reveal mobile keyboard
- Tap category dropdown to open options
- Single column layout on mobile
- Full width cards for easy reading
- Tap "Read Full Article" to open in new tab

## 🎯 Workflow Examples

### Latest Tech News
1. Select "Technology" category
2. Sort by "Latest First"
3. Load More for additional articles

### Breaking News Alert
1. Type specific topic (e.g., "breaking news")
2. Sort by "Latest First"
3. Refresh frequently for updates

### Topic Research
1. Search for topic in search box
2. Sort by "Most Relevant"
3. Load More for comprehensive coverage

## 📌 Remember

- API has daily limit (100 requests)
- Each category/search = 1 request
- Each "Load More" = 1 request
- Use wisely in production

---

**Version**: 1.0  
**Last Updated**: January 22, 2026  
**Status**: ✅ Ready to Use
