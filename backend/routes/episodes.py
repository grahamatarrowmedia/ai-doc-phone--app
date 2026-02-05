"""Episode routes."""
from flask import Blueprint, request, jsonify
from services import firestore_service as db

bp = Blueprint('episodes', __name__, url_prefix='/api/projects/<project_id>/series/<series_id>/episodes')


@bp.route('', methods=['GET'])
def list_episodes(project_id, series_id):
    """Get all episodes for a series."""
    series = db.get_series_by_id(project_id, series_id)
    if not series:
        return jsonify({'error': 'Series not found'}), 404

    episodes = db.get_episodes(project_id, series_id)
    return jsonify({'episodes': episodes})


@bp.route('', methods=['POST'])
def create_episode(project_id, series_id):
    """Create a new episode."""
    series = db.get_series_by_id(project_id, series_id)
    if not series:
        return jsonify({'error': 'Series not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'title' not in data:
        return jsonify({'error': 'Missing required field: title'}), 400

    episode = db.create_episode(project_id, series_id, {
        'title': data['title'],
        'code': data.get('code', ''),
        'brief': data.get('brief', ''),
        'current_phase': data.get('current_phase', 'research'),
        'phase_progress': data.get('phase_progress', 0)
    })
    return jsonify(episode), 201


@bp.route('/<episode_id>', methods=['GET'])
def get_episode(project_id, series_id, episode_id):
    """Get a single episode."""
    episode = db.get_episode_by_id(project_id, series_id, episode_id)
    if not episode:
        return jsonify({'error': 'Episode not found'}), 404
    return jsonify(episode)


@bp.route('/<episode_id>', methods=['PUT'])
def update_episode(project_id, series_id, episode_id):
    """Update an episode."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    episode = db.get_episode_by_id(project_id, series_id, episode_id)
    if not episode:
        return jsonify({'error': 'Episode not found'}), 404

    updated = db.update_episode(project_id, series_id, episode_id, data)
    return jsonify(updated)


@bp.route('/<episode_id>', methods=['DELETE'])
def delete_episode(project_id, series_id, episode_id):
    """Delete an episode."""
    episode = db.get_episode_by_id(project_id, series_id, episode_id)
    if not episode:
        return jsonify({'error': 'Episode not found'}), 404

    db.delete_episode(project_id, series_id, episode_id)
    return jsonify({'message': 'Episode deleted'})
