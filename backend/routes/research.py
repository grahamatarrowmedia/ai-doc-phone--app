"""Research routes."""
from flask import Blueprint, request, jsonify
from services import firestore_service as db
from services import ai_service

bp = Blueprint('research', __name__, url_prefix='/api/projects/<project_id>/series/<series_id>/episodes/<episode_id>/research')


@bp.route('', methods=['GET'])
def list_research(project_id, series_id, episode_id):
    """Get all research reports for an episode."""
    episode = db.get_episode_by_id(project_id, series_id, episode_id)
    if not episode:
        return jsonify({'error': 'Episode not found'}), 404

    reports = db.get_research_reports(project_id, series_id, episode_id)
    return jsonify({'reports': reports})


@bp.route('', methods=['POST'])
def create_research(project_id, series_id, episode_id):
    """Create a new research report (triggers AI deep research)."""
    episode = db.get_episode_by_id(project_id, series_id, episode_id)
    if not episode:
        return jsonify({'error': 'Episode not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'query' not in data:
        return jsonify({'error': 'Missing required field: query'}), 400

    # Get series for context
    series = db.get_series_by_id(project_id, series_id)

    # Get existing knowledge base
    kb_entries = db.get_knowledge_base(project_id, series_id, episode_id)

    # Run AI research
    ai_result = ai_service.deep_research(
        query=data['query'],
        series_title=series['title'],
        episode_title=episode['title'],
        episode_brief=episode.get('brief', ''),
        existing_kb=kb_entries,
        attached_files=data.get('attached_files', [])
    )

    # Create the research report
    report = db.create_research_report(project_id, series_id, episode_id, {
        'title': data['query'][:100],
        'query': data['query'],
        'type': 'ai_brief',
        'status': 'deep_research',
        'executive_summary': ai_result.get('executive_summary', ''),
        'key_findings': ai_result.get('key_findings', []),
        'bibliography': ai_result.get('bibliography', {'ai_generated': [], 'external': []}),
        'attached_files': data.get('attached_files', [])
    })

    return jsonify(report), 201


@bp.route('/<report_id>', methods=['GET'])
def get_research(project_id, series_id, episode_id, report_id):
    """Get a single research report."""
    report = db.get_research_report(project_id, series_id, episode_id, report_id)
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    return jsonify(report)


@bp.route('/<report_id>', methods=['PUT'])
def update_research(project_id, series_id, episode_id, report_id):
    """Update a research report."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    report = db.get_research_report(project_id, series_id, episode_id, report_id)
    if not report:
        return jsonify({'error': 'Report not found'}), 404

    updated = db.update_research_report(project_id, series_id, episode_id, report_id, data)
    return jsonify(updated)


@bp.route('/<report_id>/complete', methods=['POST'])
def mark_complete(project_id, series_id, episode_id, report_id):
    """Mark a research report as complete."""
    report = db.get_research_report(project_id, series_id, episode_id, report_id)
    if not report:
        return jsonify({'error': 'Report not found'}), 404

    updated = db.update_research_report(project_id, series_id, episode_id, report_id, {
        'status': 'complete'
    })
    return jsonify(updated)


@bp.route('/<report_id>/link-asset', methods=['POST'])
def link_asset(project_id, series_id, episode_id, report_id):
    """Link an archive asset to a research report."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    report = db.get_research_report(project_id, series_id, episode_id, report_id)
    if not report:
        return jsonify({'error': 'Report not found'}), 404

    linked_assets = report.get('linked_assets', [])
    linked_assets.append({
        'asset_id': data.get('asset_id'),
        'name': data.get('name'),
        'url': data.get('url'),
        'type': data.get('type')
    })

    updated = db.update_research_report(project_id, series_id, episode_id, report_id, {
        'linked_assets': linked_assets
    })
    return jsonify(updated)


# Knowledge Base routes
@bp.route('/../../knowledge-base', methods=['GET'])
def list_knowledge_base(project_id, series_id, episode_id):
    """Get all knowledge base entries for an episode."""
    episode = db.get_episode_by_id(project_id, series_id, episode_id)
    if not episode:
        return jsonify({'error': 'Episode not found'}), 404

    entries = db.get_knowledge_base(project_id, series_id, episode_id)
    return jsonify({'entries': entries})


@bp.route('/../../knowledge-base', methods=['POST'])
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
