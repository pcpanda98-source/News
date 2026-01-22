// NewsHub - State Management Store
const Store = (function(){
  let state = {
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
    }
  };
})();

// Export to global scope
window.Store = Store;

// Initialize on document ready
document.addEventListener('DOMContentLoaded', () => {
  // Load initial data
  Store.loadArticles();
  Store.loadCategories();

  // Setup global error handler
  window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    Store.addNotification('An error occurred. Please try again.', 'error');
  });
});

