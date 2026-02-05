"""Firestore database service."""
from datetime import datetime
from google.cloud import firestore

db = firestore.Client()


def get_timestamp():
    """Get current timestamp in ISO format."""
    return datetime.utcnow().isoformat() + 'Z'


# Projects
def get_projects():
    """Get all projects."""
    projects_ref = db.collection('projects')
    docs = projects_ref.stream()
    return [{'id': doc.id, **doc.to_dict()} for doc in docs]


def get_project(project_id):
    """Get a single project by ID."""
    doc = db.collection('projects').document(project_id).get()
    if not doc.exists:
        return None
    return {'id': doc.id, **doc.to_dict()}


def create_project(data):
    """Create a new project."""
    data['created_at'] = get_timestamp()
    data['updated_at'] = get_timestamp()
    doc_ref = db.collection('projects').document()
    doc_ref.set(data)
    return {'id': doc_ref.id, **data}


def update_project(project_id, data):
    """Update a project."""
    data['updated_at'] = get_timestamp()
    db.collection('projects').document(project_id).update(data)
    return get_project(project_id)


def delete_project(project_id):
    """Delete a project."""
    db.collection('projects').document(project_id).delete()


# Series
def get_series(project_id):
    """Get all series for a project."""
    series_ref = db.collection('projects').document(project_id).collection('series')
    docs = series_ref.order_by('order').stream()
    return [{'id': doc.id, **doc.to_dict()} for doc in docs]


def get_series_by_id(project_id, series_id):
    """Get a single series by ID."""
    doc = db.collection('projects').document(project_id).collection('series').document(series_id).get()
    if not doc.exists:
        return None
    return {'id': doc.id, **doc.to_dict()}


def create_series(project_id, data):
    """Create a new series."""
    data['created_at'] = get_timestamp()
    # Get next order number
    existing = get_series(project_id)
    data['order'] = len(existing) + 1
    doc_ref = db.collection('projects').document(project_id).collection('series').document()
    doc_ref.set(data)
    return {'id': doc_ref.id, **data}


def update_series(project_id, series_id, data):
    """Update a series."""
    data['updated_at'] = get_timestamp()
    db.collection('projects').document(project_id).collection('series').document(series_id).update(data)
    return get_series_by_id(project_id, series_id)


def delete_series(project_id, series_id):
    """Delete a series."""
    db.collection('projects').document(project_id).collection('series').document(series_id).delete()


# Episodes
def get_episodes(project_id, series_id):
    """Get all episodes for a series."""
    episodes_ref = db.collection('projects').document(project_id).collection('series').document(series_id).collection('episodes')
    docs = episodes_ref.order_by('order').stream()
    return [{'id': doc.id, **doc.to_dict()} for doc in docs]


def get_episode_by_id(project_id, series_id, episode_id):
    """Get a single episode by ID."""
    doc = db.collection('projects').document(project_id).collection('series').document(series_id).collection('episodes').document(episode_id).get()
    if not doc.exists:
        return None
    return {'id': doc.id, **doc.to_dict()}


def create_episode(project_id, series_id, data):
    """Create a new episode."""
    data['created_at'] = get_timestamp()
    data['current_phase'] = data.get('current_phase', 'research')
    data['phase_progress'] = data.get('phase_progress', 0)
    # Get next order number
    existing = get_episodes(project_id, series_id)
    data['order'] = len(existing) + 1
    doc_ref = db.collection('projects').document(project_id).collection('series').document(series_id).collection('episodes').document()
    doc_ref.set(data)
    return {'id': doc_ref.id, **data}


def update_episode(project_id, series_id, episode_id, data):
    """Update an episode."""
    data['updated_at'] = get_timestamp()
    db.collection('projects').document(project_id).collection('series').document(series_id).collection('episodes').document(episode_id).update(data)
    return get_episode_by_id(project_id, series_id, episode_id)


def delete_episode(project_id, series_id, episode_id):
    """Delete an episode."""
    db.collection('projects').document(project_id).collection('series').document(series_id).collection('episodes').document(episode_id).delete()


# Research
def get_research_reports(project_id, series_id, episode_id):
    """Get all research reports for an episode."""
    research_ref = db.collection('projects').document(project_id).collection('series').document(series_id).collection('episodes').document(episode_id).collection('research')
    docs = research_ref.order_by('created_at', direction=firestore.Query.DESCENDING).stream()
    return [{'id': doc.id, **doc.to_dict()} for doc in docs]


def get_research_report(project_id, series_id, episode_id, report_id):
    """Get a single research report by ID."""
    doc = db.collection('projects').document(project_id).collection('series').document(series_id).collection('episodes').document(episode_id).collection('research').document(report_id).get()
    if not doc.exists:
        return None
    return {'id': doc.id, **doc.to_dict()}


def create_research_report(project_id, series_id, episode_id, data):
    """Create a new research report."""
    data['created_at'] = get_timestamp()
    data['updated_at'] = get_timestamp()
    data['status'] = data.get('status', 'in_progress')
    data['type'] = data.get('type', 'ai_brief')
    data['producer_notes'] = data.get('producer_notes', '')
    data['linked_assets'] = data.get('linked_assets', [])
    doc_ref = db.collection('projects').document(project_id).collection('series').document(series_id).collection('episodes').document(episode_id).collection('research').document()
    doc_ref.set(data)
    return {'id': doc_ref.id, **data}


def update_research_report(project_id, series_id, episode_id, report_id, data):
    """Update a research report."""
    data['updated_at'] = get_timestamp()
    db.collection('projects').document(project_id).collection('series').document(series_id).collection('episodes').document(episode_id).collection('research').document(report_id).update(data)
    return get_research_report(project_id, series_id, episode_id, report_id)


# Knowledge Base
def get_knowledge_base(project_id, series_id, episode_id):
    """Get all knowledge base entries for an episode."""
    kb_ref = db.collection('projects').document(project_id).collection('series').document(series_id).collection('episodes').document(episode_id).collection('knowledge_base')
    docs = kb_ref.stream()
    return [{'id': doc.id, **doc.to_dict()} for doc in docs]


def add_to_knowledge_base(project_id, series_id, episode_id, data):
    """Add an entry to the knowledge base."""
    data['created_at'] = get_timestamp()
    doc_ref = db.collection('projects').document(project_id).collection('series').document(series_id).collection('episodes').document(episode_id).collection('knowledge_base').document()
    doc_ref.set(data)
    return {'id': doc_ref.id, **data}
