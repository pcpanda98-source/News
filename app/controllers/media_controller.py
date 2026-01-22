from flask import Blueprint, render_template, request, jsonify
from app.services.media_service import list_media, create_media, delete_media, count_media
import os
import uuid
from datetime import datetime


media_bp = Blueprint('media', __name__, template_folder='templates')


@media_bp.route('/media/manage')
def manage():
    """Render the media management page"""
    media = list_media()
    return render_template('manage_media.html', media=media)


@media_bp.route('/api/media', methods=['GET'])
def list_media_api():
    """List all media files"""
    media = list_media()
    return jsonify({
        'media': [m.to_dict() for m in media],
        'count': len(media)
    })


@media_bp.route('/api/media', methods=['POST'])
def upload_media():
    """Upload a new media file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check allowed extensions
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}
    file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    
    if file_ext not in allowed_extensions:
        return jsonify({'error': f'Invalid file type. Allowed: {", ".join(allowed_extensions)}'}), 400
    
    # Create uploads directory if it doesn't exist (use project's static folder)
    upload_folder = '/workspaces/News/static/uploads'
    os.makedirs(upload_folder, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_filename = f"{timestamp}_{uuid.uuid4().hex[:8]}.{file_ext}"
    file_path = os.path.join(upload_folder, unique_filename)
    
    # Save the file
    file.save(file_path)
    
    # Get file info
    file_size = os.path.getsize(file_path)
    
    # Create database record
    media = create_media(
        filename=unique_filename,
        original_name=file.filename,
        file_type=file.content_type or f'image/{file_ext}',
        file_size=file_size,
        file_path=file_path
    )
    
    return jsonify({
        'success': True,
        'media': media.to_dict()
    }), 201


@media_bp.route('/api/media/<int:media_id>', methods=['DELETE'])
def delete_media_api(media_id):
    """Delete a media file"""
    success = delete_media(media_id)
    
    if success:
        return jsonify({'success': True, 'message': 'Media deleted successfully'})
    else:
        return jsonify({'error': 'Media not found'}), 404


@media_bp.route('/api/media/count')
def media_count():
    """Get total count of media files"""
    return jsonify({'count': count_media()})

