# Manage News - Quick Reference

## Access Points

| Location | URL | Method |
|----------|-----|--------|
| Main Navigation (Desktop) | `/manage` | Click purple "⚙️ Manage News" button |
| Main Navigation (Mobile) | `/manage` | Menu → Manage News |
| Articles Page | `/manage` | Click "⚙️ Manage News" button in header |
| Direct Link | `http://127.0.0.1:8080/manage` | Browser address bar |

## Key Features at a Glance

### Search & Filter
- **Search Box**: Filter articles by title in real-time
- **Category Filter**: Select category to view only those articles
- **Sort Options**: Newest, Oldest, or Alphabetical order
- **Reset Button**: Clear all filters

### Table Columns
| Column | Description |
|--------|-------------|
| ID | Article unique identifier |
| Title | Article title with preview |
| Category | Badge showing assigned category |
| Created | Article creation date |
| Preview | Character count |
| Actions | View, Edit, Delete buttons |

### Available Actions

#### 👁️ View
- Opens article detail page
- Read full article content
- See related articles

#### ✏️ Edit
- Opens edit modal
- Modify title, category, content
- Real-time character counter
- Save changes to database

#### 🗑️ Delete
- Confirmation dialog required
- Permanently removes article
- Success notification on completion

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Focus search | Ctrl+F (browser search) |
| Select next field | Tab |
| Submit form | Enter |
| Close modal | Esc (custom - click outside modal) |

## Common Tasks

### Find an Article
1. Type article name in search box
2. Results filter immediately
3. Click "View", "Edit", or "Delete"

### Create New Article
1. Click "➕ Create New Article" button (top right)
2. Go to `/articles/create`
3. Fill in form and submit

### Edit Article Details
1. Find article using search/filters
2. Click "✏️ Edit" button
3. Update fields in modal
4. Click "Save Changes"
5. Confirm changes in notification

### Delete Article
1. Find article using search/filters
2. Click "🗑️ Delete" button
3. Confirm in dialog
4. Article removed immediately

### View Specific Category
1. Open category dropdown
2. Select desired category
3. Table shows only matching articles
4. Reset to see all categories

### Sort All Articles
1. Open sort dropdown
2. Choose: Newest First, Oldest First, or Alphabetical
3. Table reorganizes instantly

## Dashboard Stats (Bottom Section)

Shows real-time information:
- **Total Articles**: Count of all articles in database
- **Total Categories**: Count of all categories
- **Database Usage**: Percentage of database capacity used

## Color Legend

| Color | Meaning |
|-------|---------|
| 🔵 Blue | Primary/Read actions |
| 🟢 Green | Success/View actions |
| 🔴 Red | Dangerous/Delete actions |
| 🟣 Purple | Admin/Manage actions |
| ⚪ Gray | Secondary/Reset actions |

## Table Row Interaction

- Hover over a row → Background highlights
- Click ID → Shows article ID
- Click Title → Shows preview text
- Category shows with colored badge
- All actions in rightmost column

## Error Messages & Solutions

| Issue | Solution |
|-------|----------|
| Modal won't open | Refresh page, check console |
| Edit saves but doesn't update | Wait for auto-refresh |
| Search shows no results | Clear search box or change text |
| Delete button inactive | Ensure JavaScript enabled |
| Styling looks broken | Hard refresh: Ctrl+Shift+R |

## Tips & Tricks

✨ **Pro Tips**

1. **Quick Edit**: Double-click row might open edit (not implemented, but planned)
2. **Bulk Operations**: Hold Shift to select multiple articles (planned feature)
3. **Export Data**: Right-click table → Export as CSV (future feature)
4. **Keyboard Nav**: Use Tab to navigate form fields in modal
5. **Mobile Friendly**: Swipe left on table row for more options (planned)

## Related Pages Quick Links

- 🏠 [Home](/)
- 📰 [Articles](/articles)
- 📁 [Categories](/categories)
- ✏️ [Create Article](/articles/create)
- ⚙️ [Manage Categories](/categories/manage)

## File Locations (Developer Reference)

| File | Path |
|------|------|
| Template | `/app/templates/manage_articles.html` |
| Route | `/app/controllers/article_controller.py` - Line ~38 |
| API Endpoints | `/app/controllers/article_controller.py` - Lines ~48-56 |
| Service Layer | `/app/services/article_service.py` |
| Styling | `/static/css/style.css` |
| JavaScript | Embedded in template |

## API Endpoints

### List Articles
```
GET /api/articles
Response: JSON array of articles
```

### Update Article
```
PUT /api/articles/{id}
Body: { "title": "...", "content": "...", "category_id": 1 }
Response: Updated article or 404
```

### Delete Article
```
DELETE /api/articles/{id}
Response: 204 (success) or 404 (not found)
```

## Performance

- **Search**: Real-time (client-side) - instant results
- **Edit**: Form modal - lightweight
- **Delete**: AJAX with visual feedback
- **Load Time**: Typically < 1 second
- **Memory**: Optimized for hundreds of articles

## Browser Support

| Browser | Support | Notes |
|---------|---------|-------|
| Chrome | ✅ Full | Recommended |
| Firefox | ✅ Full | Fully compatible |
| Safari | ✅ Full | Mobile & desktop |
| Edge | ✅ Full | Modern versions |
| IE 11 | ❌ None | Not supported |

## Support & Troubleshooting

### Page won't load
- Check Flask server is running: `http://127.0.0.1:8080`
- Verify template file exists: `/app/templates/manage_articles.html`
- Check browser console for errors (F12)

### Features not working
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh page (Ctrl+Shift+R)
- Check JavaScript errors in console

### Database not updating
- Verify Flask app is running
- Check API endpoints respond: `/api/articles`
- Review Flask logs for errors

### Styling issues
- Ensure Tailwind CDN is loaded
- Check custom CSS file: `/static/css/style.css`
- Clear browser cache

---

**Last Updated**: January 22, 2026
**Version**: 1.0
**Status**: Production Ready ✅
