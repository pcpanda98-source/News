// NewsHub - State Management Store
const Store = (function(){
  let state = {
    articles: [],
    categories: [],
    currentUser: null,
    notifications: [],
    bookmarks: [], // Bookmarked article IDs
    filters: {
      searchTerm: '',
      selectedCategory: null,
      sortBy: 'recent'
    }
  };

  const subs = {};

  return {
    // Get state value
    get(key) {
      return state[key];
    },

    // Set state value and notify subscribers
    set(key, value) {
      state[key] = value;
      if (subs[key]) {
        subs[key].forEach(fn => fn(value));
      }
    },

    // Subscribe to state changes
    subscribe(key, callback) {
      if (!subs[key]) {
        subs[key] = [];
      }
      subs[key].push(callback);
    },

    // Update nested state
    update(key, updates) {
      state[key] = { ...state[key], ...updates };
      if (subs[key]) {
        subs[key].forEach(fn => fn(state[key]));
      }
    },

    // Get entire state
    getState() {
      return JSON.parse(JSON.stringify(state));
    },

    // Reset state
    reset() {
      state = {
        articles: [],
        categories: [],
        currentUser: null,
        notifications: [],
        filters: {
          searchTerm: '',
          selectedCategory: null,
          sortBy: 'recent'
        }
      };
    },

    // Load articles
    async loadArticles() {
      try {
        const response = await fetch('/api/articles');
        const articles = await response.json();
        this.set('articles', articles);
        return articles;
      } catch (error) {
        console.error('Error loading articles:', error);
        return [];
      }
    },

    // Load categories
    async loadCategories() {
      try {
        const response = await fetch('/api/categories');
        
        // Check if response is OK
        if (!response.ok) {
          console.error('Error loading categories: HTTP', response.status);
          return [];
        }
        
        // Check content type to ensure it's JSON
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
          console.error('Error loading categories: Expected JSON but got', contentType);
          return [];
        }
        
        const categories = await response.json();
        this.set('categories', categories);
        return categories;
      } catch (error) {
        console.error('Error loading categories:', error);
        return [];
      }
    },

    // Add notification
    addNotification(message, type = 'info', duration = 3000) {
      const id = Date.now();
      const notification = { id, message, type };
      
      const currentNotifications = state.notifications || [];
      this.set('notifications', [...currentNotifications, notification]);

      if (duration > 0) {
        setTimeout(() => {
          this.removeNotification(id);
        }, duration);
      }

      return id;
    },

    // Remove notification
    removeNotification(id) {
      const currentNotifications = state.notifications || [];
      this.set('notifications', currentNotifications.filter(n => n.id !== id));
    },

    // ============ BOOKMARK FUNCTIONS ============
    
    // Load bookmarks from localStorage
    loadBookmarks() {
      try {
        const saved = localStorage.getItem('news_bookmarks');
        if (saved) {
          const bookmarks = JSON.parse(saved);
          state.bookmarks = bookmarks;
        }
      } catch (error) {
        console.error('Error loading bookmarks:', error);
        state.bookmarks = [];
      }
    },

    // Save bookmarks to localStorage
    saveBookmarks() {
      try {
        localStorage.setItem('news_bookmarks', JSON.stringify(state.bookmarks));
      } catch (error) {
        console.error('Error saving bookmarks:', error);
      }
    },

    // Check if an article is bookmarked
    isBookmarked(articleId) {
      return state.bookmarks.includes(parseInt(articleId));
    },

    // Toggle bookmark for an article
    toggleBookmark(articleId) {
      const id = parseInt(articleId);
      const index = state.bookmarks.indexOf(id);
      
      if (index === -1) {
        // Add to bookmarks
        state.bookmarks.push(id);
        this.saveBookmarks();
        this.addNotification('Article bookmarked!', 'success', 2000);
        return true; // Now bookmarked
      } else {
        // Remove from bookmarks
        state.bookmarks.splice(index, 1);
        this.saveBookmarks();
        this.addNotification('Bookmark removed', 'info', 2000);
        return false; // No longer bookmarked
      }
    },

    // Get all bookmarked articles
    getBookmarkedArticles() {
      return state.articles.filter(article => state.bookmarks.includes(article.id));
    },

    // Remove bookmark
    removeBookmark(articleId) {
      const id = parseInt(articleId);
      const index = state.bookmarks.indexOf(id);
      if (index !== -1) {
        state.bookmarks.splice(index, 1);
        this.saveBookmarks();
      }
    },

    // Clear all bookmarks
    clearBookmarks() {
      state.bookmarks = [];
      this.saveBookmarks();
      this.addNotification('All bookmarks cleared', 'info', 2000);
    },

    // Get bookmark count
    getBookmarkCount() {
      return state.bookmarks.length;
    }
  };
})();

// Export to global scope
window.Store = Store;

// Initialize on document ready
document.addEventListener('DOMContentLoaded', () => {
  // Load initial data
  Store.loadBookmarks(); // Load bookmarks first
  Store.loadArticles();
  Store.loadCategories();

  // Setup global error handler
  window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    Store.addNotification('An error occurred. Please try again.', 'error');
  });
});

