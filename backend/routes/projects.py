"""Project routes."""
from flask import Blueprint, request, jsonify
from services import firestore_service as db

bp = Blueprint('projects', __name__, url_prefix='/api/projects')


@bp.route('', methods=['GET'])
def list_projects():
    """Get all projects."""
    projects = db.get_projects()
    return jsonify({'projects': projects})


@bp.route('', methods=['POST'])
def create_project():
    """Create a new project."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    required = ['name', 'type']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    project = db.create_project({
        'name': data['name'],
        'type': data['type'],
        'description': data.get('description', ''),
        'producer': data.get('producer', {'name': 'Unknown', 'role': 'PRODUCER'})
    })
    return jsonify(project), 201


@bp.route('/<project_id>', methods=['GET'])
def get_project(project_id):
    """Get a single project."""
    project = db.get_project(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    return jsonify(project)


@bp.route('/<project_id>', methods=['PUT'])
def update_project(project_id):
    """Update a project."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    project = db.get_project(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    updated = db.update_project(project_id, data)
    return jsonify(updated)


@bp.route('/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Delete a project."""
    project = db.get_project(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    db.delete_project(project_id)
    return jsonify({'message': 'Project deleted'})
