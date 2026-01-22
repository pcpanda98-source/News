# Manage News - Feature Documentation

## Overview
The "Manage News" feature provides an admin interface for managing articles. It integrates seamlessly with the existing Categories and Articles pages, offering complete CRUD (Create, Read, Update, Delete) operations for articles.

## Features

### 1. **Article Listing & Search**
- View all articles in a responsive table format
- Real-time search by article title
- Filter articles by category
- Sort articles by:
  - Newest First (recent)
  - Oldest First (oldest)
  - Alphabetical Order (title)

### 2. **Article Operations**
- **View**: Direct link to article detail page
- **Edit**: Inline modal editor for article title, content, and category
- **Delete**: With confirmation dialog to prevent accidental deletion
- **Create**: Quick link to create new articles

### 3. **Responsive Design**
- Mobile-first Tailwind CSS design
- Horizontal scroll table on smaller screens
- Touch-friendly buttons and modals
- Responsive filter bar

### 4. **Statistics Dashboard**
- Total articles count
- Total categories count
- Database usage percentage

## File Structure

### Backend Files

#### 1. **article_controller.py**
```python
@article_bp.route('/manage')
def manage_articles():
    """Display manage articles page with all articles and categories"""
    articles = list_articles()
    categories = list_categories()
    return render_template('manage_articles.html', articles=articles, categories=categories)
```

**Route Added:**
- `GET /manage` - Display manage articles page

**Existing API Endpoints Used:**
- `PUT /api/articles/<id>` - Update article
- `DELETE /api/articles/<id>` - Delete article
- `GET /api/articles` - List articles

### Frontend Files

#### 2. **manage_articles.html**
Location: `/app/templates/manage_articles.html`

**Key Sections:**
1. **Header** - Title, description, and create new article button
2. **Filter Bar** - Search, category filter, sort options, and reset button
3. **Statistics** - Total articles, categories, and database usage
4. **Articles Table** - Responsive table with all article information
5. **Edit Modal** - Form for editing article details
6. **Empty State** - Message when no articles exist

**Block Inheritance:**
- Extends: `layout.html`
- Custom blocks: `{% block content %}`, `{% block scripts %}`

#### 3. **Modified layout.html**
Added navigation links:
- Desktop: `<a href="/manage">Manage News</a>`
- Mobile: Menu item for "Manage News"

#### 4. **Modified articles.html**
Added "Manage News" button in header for quick access to admin panel

## JavaScript Functionality

### Core Functions

```javascript
// Edit article - opens modal with article data
editArticle(id, title, categoryId, content)

// Close edit modal
closeEditModal()

// Update character count in edit form
updateCharCount()

// Submit edited article via PUT request
submitEdit(event)

// Delete article with confirmation dialog
deleteArticle(id)

// Show toast notifications
showNotification(message, type, duration)

// Filter and sort articles
filterAndSort()

// Reset all filters to default state
resetFilters()

// Update statistics display
updateStats()
```

### Event Listeners
- `searchInput` - Real-time filtering as user types
- `categoryFilter` - Filter articles by selected category
- `sortFilter` - Sort articles by selected criteria
- `editContent` - Update character count
- Modal click outside - Close edit modal

## API Endpoints Used

### 1. GET /api/articles
**Purpose:** Fetch list of all articles
**Response:** JSON array of article objects

### 2. PUT /api/articles/{id}
**Purpose:** Update an article
**Request Body:**
```json
{
  "title": "Updated Title",
  "content": "Updated content...",
  "category_id": 1
}
```
**Response:** Updated article object or 404

### 3. DELETE /api/articles/{id}
**Purpose:** Delete an article
**Response:** 204 No Content or 404

## Database Models Used

### Article Model
- `id` - Primary key
- `title` - Article title
- `content` - Article body text
- `category_id` - Foreign key to Category
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp
- `category` - Relationship to Category

### Category Model
- `id` - Primary key
- `name` - Category name

## Navigation Integration

### Links to Manage News Page
1. **Main Navigation** (Desktop & Mobile):
   - Added purple button: "⚙️ Manage News"
   - Path: `/manage`

2. **Articles Listing Page**:
   - Header button: "⚙️ Manage News"
   - Quick access from articles view

3. **Manage Articles Page**:
   - "Create New Article" button leads to `/articles/create`
   - "Back to Articles" link leads to `/articles`

## UI/UX Features

### Color Coding
- **Blue** - Primary actions (edit, view)
- **Green** - Positive actions (view article)
- **Red** - Destructive actions (delete)
- **Purple** - Admin/manage actions
- **Gray** - Secondary actions (reset, cancel)

### Visual Feedback
- Hover effects on table rows
- Smooth transitions for buttons
- Animation for deleted articles (fade out + slide)
- Toast notifications for success/error messages
- Character count updates in real-time

### Accessibility
- Semantic HTML5 structure
- ARIA labels on buttons
- Keyboard-friendly form inputs
- Clear visual hierarchy with proper heading levels

## How to Use

### Search Articles
1. Enter keyword in search box
2. Results filter in real-time
3. Clear search to show all

### Filter by Category
1. Select category from dropdown
2. Table updates to show matching articles
3. Select "All Categories" to reset

### Sort Articles
1. Select sort option from dropdown
2. Options: Newest First, Oldest First, Alphabetical
3. Table reorders automatically

### Edit Article
1. Click "✏️ Edit" button on article row
2. Modal opens with article details
3. Update title, category, or content
4. Click "Save Changes" to submit
5. Page refreshes with updated article

### Delete Article
1. Click "🗑️ Delete" button on article row
2. Confirmation dialog appears
3. Confirm deletion
4. Article is removed from table
5. Success notification appears

### Create New Article
1. Click "Create New Article" button
2. Redirects to `/articles/create`
3. Fill in article form
4. Submit to create new article

## Performance Features

### Efficient Filtering
- Client-side filtering for instant response
- No page reload needed
- Data already loaded on initial page

### Debounced Operations
- Uses store pattern for state management
- Reactive updates without full page refresh
- Smooth animations during operations

### Responsive Table
- Horizontal scroll on mobile devices
- Truncated text with ellipsis
- All controls accessible on small screens

## Security Considerations

### Input Validation
- Form fields have `required` attributes
- Server-side validation in API endpoints
- SQL injection prevention via ORM

### CSRF Protection
- Flask handles CSRF tokens
- API requests validated by backend

### Authorization
- Consider adding role-based access control
- Admin-only access to manage pages
- User authentication recommended for production

## Error Handling

### Network Errors
- Caught with `.catch()` in fetch calls
- User-friendly error messages
- Notifications display failure reasons

### Validation Errors
- Client-side: Required field checks
- Server-side: Model validation

### Confirmation Dialogs
- Prevents accidental deletion
- Users must confirm before permanent actions

## Browser Compatibility

- Chrome/Edge (recommended)
- Firefox
- Safari
- Mobile browsers (iOS Safari, Chrome Mobile)

## Testing Recommendations

### Manual Testing
- [ ] Create new article
- [ ] Search for article by title
- [ ] Filter by category
- [ ] Sort by different options
- [ ] Edit article and verify changes
- [ ] Delete article with confirmation
- [ ] Test on mobile browser
- [ ] Test with long article titles
- [ ] Verify all links work

### Automated Testing
- Unit tests for filter functions
- Integration tests for API calls
- E2E tests for complete workflows

## Future Enhancements

1. **Bulk Operations**
   - Select multiple articles
   - Bulk delete
   - Bulk category assignment

2. **Advanced Filtering**
   - Date range filtering
   - Author filtering
   - Status filtering (draft, published)

3. **Import/Export**
   - Export articles as CSV
   - Bulk import from CSV

4. **Scheduling**
   - Schedule article publication
   - Auto-archive old articles

5. **Analytics**
   - View count tracking
   - Most viewed articles
   - Article performance metrics

6. **Versioning**
   - Article revision history
   - Rollback to previous versions
   - Change tracking

## Troubleshooting

### Edit modal won't open
- Check browser console for JavaScript errors
- Verify Flask server is running
- Ensure article data is properly formatted

### Delete not working
- Confirm browser has JavaScript enabled
- Check network tab for API errors
- Verify article ID is correct

### Search/filter not updating
- Ensure all articles loaded from server
- Check that data attributes are set correctly
- Verify filter functions are bound to inputs

### Styling issues
- Clear browser cache (Ctrl+Shift+Delete)
- Reload page (Ctrl+R or Cmd+Shift+R)
- Check that Tailwind CDN is loaded

## Related Pages

- [Articles Page](/articles) - View public articles
- [Article Detail](/articles/{id}) - View single article
- [Create Article](/articles/create) - Create new article
- [Categories](/categories) - View categories
- [Manage Categories](/categories/manage) - Manage categories
