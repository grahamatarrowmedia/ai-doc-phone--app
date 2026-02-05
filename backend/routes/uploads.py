"""File upload routes."""
import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from services import storage_service as storage

bp = Blueprint('uploads', __name__, url_prefix='/api')

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'mp3', 'wav', 'doc', 'docx', 'txt'}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/upload', methods=['POST'])
def upload_file():
    """Upload a file to GCS."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': f'File type not allowed. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400

    # Get optional path prefix from form data
    project_id = request.form.get('project_id', 'general')
    series_id = request.form.get('series_id', '')
    episode_id = request.form.get('episode_id', '')

    # Build destination path
    path_parts = ['uploads', project_id]
    if series_id:
        path_parts.append(series_id)
    if episode_id:
        path_parts.append(episode_id)

    filename = secure_filename(file.filename)
    destination_path = '/'.join(path_parts) + '/' + filename

    try:
        result = storage.upload_file(file, destination_path)
        return jsonify({
            'message': 'File uploaded successfully',
            'file': {
                'name': filename,
                'url': result['url'],
                'path': result['path'],
                'size': result['size'],
                'content_type': result['content_type']
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
