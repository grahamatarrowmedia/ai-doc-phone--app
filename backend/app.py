"""AiM Studio - Intelligent Documentary Workflow Backend."""
import os
import sys

# Add backend directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config

# Import route blueprints
from routes.projects import bp as projects_bp
from routes.series import bp as series_bp
from routes.episodes import bp as episodes_bp
from routes.research import bp as research_bp
from routes.uploads import bp as uploads_bp

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
app.config.from_object(Config)

# Enable CORS for development
CORS(app, origins=['http://localhost:3000', 'http://localhost:3001', 'http://127.0.0.1:3000', 'http://127.0.0.1:3001'])

# Register blueprints
app.register_blueprint(projects_bp)
app.register_blueprint(series_bp)
app.register_blueprint(episodes_bp)
app.register_blueprint(research_bp)
app.register_blueprint(uploads_bp)

# Knowledge Base routes (separate from research for cleaner URLs)
from flask import Blueprint, request, jsonify
from services import firestore_service as db

kb_bp = Blueprint('knowledge_base', __name__, url_prefix='/api/projects/<project_id>/series/<series_id>/episodes/<episode_id>/knowledge-base')


@kb_bp.route('', methods=['GET'])
def list_knowledge_base(project_id, series_id, episode_id):
    """Get all knowledge base entries for an episode."""
    episode = db.get_episode_by_id(project_id, series_id, episode_id)
    if not episode:
        return jsonify({'error': 'Episode not found'}), 404
    entries = db.get_knowledge_base(project_id, series_id, episode_id)
    return jsonify({'entries': entries})


@kb_bp.route('', methods=['POST'])
def add_to_knowledge_base(project_id, series_id, episode_id):
    """Add an entry to the knowledge base."""
    episode = db.get_episode_by_id(project_id, series_id, episode_id)
    if not episode:
        return jsonify({'error': 'Episode not found'}), 404

    data = request.get_json()
    if not data or 'fact' not in data:
        return jsonify({'error': 'Missing required field: fact'}), 400

    entry = db.add_to_knowledge_base(project_id, series_id, episode_id, {
        'fact': data['fact'],
        'source_report_id': data.get('source_report_id'),
        'source_indices': data.get('source_indices', []),
        'confidence': data.get('confidence', 'medium'),
        'category': data.get('category', 'general')
    })
    return jsonify(entry), 201


app.register_blueprint(kb_bp)


# Health check endpoint
@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'aim-studio'})


# Serve React app in production
@app.route('/')
def serve_index():
    """Serve the React app."""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files or fall back to index.html for client-side routing."""
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
