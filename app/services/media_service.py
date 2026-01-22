from app.models.media import Media
from app.models.db import db
import os


def list_media():
    """Get all media files ordered by upload date (newest first)"""
    return Media.query.order_by(Media.uploaded_at.desc()).all()


def get_media(media_id):
    """Get a single media file by ID"""
    return Media.query.get(media_id)


def create_media(filename, original_name, file_type, file_size, file_path):
    """Create a new media record"""
    media = Media(
        filename=filename,
        original_name=original_name,
        file_type=file_type,
        file_size=file_size,
        file_path=file_path
    )
    db.session.add(media)
    db.session.commit()
    return media


def delete_media(media_id):
    """Delete a media file and its database record"""
    media = get_media(media_id)
    if not media:
        return False
    
    # Delete the physical file
    try:
        if os.path.exists(media.file_path):
            os.remove(media.file_path)
    except OSError:
        pass  # File might already be deleted
    
    # Delete the database record
    db.session.delete(media)
    db.session.commit()
    return True


def get_media_by_filename(filename):
    """Get media by filename"""
    return Media.query.filter_by(filename=filename).first()


def count_media():
    """Get total count of media files"""
    return Media.query.count()

