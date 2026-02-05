"""Series routes."""
from flask import Blueprint, request, jsonify
from services import firestore_service as db

bp = Blueprint('series', __name__, url_prefix='/api/projects/<project_id>/series')


@bp.route('', methods=['GET'])
def list_series(project_id):
    """Get all series for a project."""
    project = db.get_project(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    series = db.get_series(project_id)
    return jsonify({'series': series})


@bp.route('', methods=['POST'])
def create_series(project_id):
    """Create a new series."""
    project = db.get_project(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'title' not in data:
        return jsonify({'error': 'Missing required field: title'}), 400

    series = db.create_series(project_id, {
        'title': data['title'],
        'description': data.get('description', '')
    })
    return jsonify(series), 201


@bp.route('/<series_id>', methods=['GET'])
def get_series(project_id, series_id):
    """Get a single series."""
    series = db.get_series_by_id(project_id, series_id)
    if not series:
        return jsonify({'error': 'Series not found'}), 404
    return jsonify(series)


@bp.route('/<series_id>', methods=['PUT'])
def update_series(project_id, series_id):
    """Update a series."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    series = db.get_series_by_id(project_id, series_id)
    if not series:
        return jsonify({'error': 'Series not found'}), 404

    updated = db.update_series(project_id, series_id, data)
    return jsonify(updated)


@bp.route('/<series_id>', methods=['DELETE'])
def delete_series(project_id, series_id):
    """Delete a series."""
    series = db.get_series_by_id(project_id, series_id)
    if not series:
        return jsonify({'error': 'Series not found'}), 404

    db.delete_series(project_id, series_id)
    return jsonify({'message': 'Series deleted'})
