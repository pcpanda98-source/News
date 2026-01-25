#!/usr/bin/env python3
"""
Migration script to add author and updated_at columns to the articles table.
Run this script to update the database schema for the new author field.
"""

from app.models.db import db
from app.models.article import Article
from sqlalchemy import text

def migrate_author_column():
    """Add author and updated_at columns to the articles table."""
    
    # Check if the column already exists
    check_query = text("SELECT name FROM pragma_table_info('articles') WHERE name='author'")
    result = db.session.execute(check_query).fetchone()
    
    if result:
        print("✓ Author column already exists in articles table.")
    else:
        # Add author column
        add_author = text("ALTER TABLE articles ADD COLUMN author VARCHAR(100)")
        db.session.execute(add_author)
        db.session.commit()
        print("✓ Added 'author' column to articles table.")
    
    # Check if updated_at column exists
    check_updated = text("SELECT name FROM pragma_table_info('articles') WHERE name='updated_at'")
    result_updated = db.session.execute(check_updated).fetchone()
    
    if result_updated:
        print("✓ Updated_at column already exists in articles table.")
    else:
        # Add updated_at column
        add_updated = text("ALTER TABLE articles ADD COLUMN updated_at TIMESTAMP")
        db.session.execute(add_updated)
        db.session.commit()
        print("✓ Added 'updated_at' column to articles table.")
    
    print("\n✓ Migration completed successfully!")
    print("\nNote: Existing articles will have null/empty author values.")
    print("You can now add authors to articles through the Create Article page.")

if __name__ == '__main__':
    # Import the app context
    from app import create_app
    import sys
    
    app = create_app()
    with app.app_context():
        try:
            migrate_author_column()
            sys.exit(0)
        except Exception as e:
            print(f"\n✗ Migration failed: {e}")
            sys.exit(1)

