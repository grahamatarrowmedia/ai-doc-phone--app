"""Data schemas for AiM Studio."""

# Project schema
PROJECT_SCHEMA = {
    'name': str,        # Required
    'type': str,        # Required (e.g., 'DOCUMENTARY')
    'description': str, # Optional
    'producer': {
        'name': str,
        'role': str
    },
    'created_at': str,  # ISO timestamp
    'updated_at': str   # ISO timestamp
}

# Series schema
SERIES_SCHEMA = {
    'title': str,       # Required
    'description': str, # Optional
    'order': int,       # Position in project
    'created_at': str
}

# Episode schema
EPISODE_SCHEMA = {
    'title': str,           # Required
    'code': str,            # e.g., 'EP01'
    'brief': str,           # Episode brief/description
    'current_phase': str,   # 'research', 'archive', 'scripting', 'interviews', 'voiceover', 'assembly', 'review'
    'phase_progress': int,  # 0-100 percentage
    'order': int,
    'created_at': str,
    'updated_at': str
}

# Research report schema
RESEARCH_SCHEMA = {
    'title': str,               # Truncated query
    'query': str,               # Full research query
    'type': str,                # 'ai_brief' or 'manual'
    'status': str,              # 'deep_research', 'in_progress', 'complete'
    'executive_summary': str,   # AI-generated summary
    'key_findings': [           # List of findings
        {
            'name': str,
            'description': str,
            'source_indices': [int],
            'confidence': str   # 'high', 'medium', 'low'
        }
    ],
    'producer_notes': str,      # User annotations
    'linked_assets': [          # Linked archive assets
        {
            'asset_id': str,
            'name': str,
            'url': str,
            'type': str
        }
    ],
    'bibliography': {
        'ai_generated': [str],
        'external': [str]
    },
    'attached_files': [         # Files attached to research query
        {
            'name': str,
            'url': str,
            'type': str
        }
    ],
    'created_at': str,
    'updated_at': str
}

# Knowledge base entry schema
KNOWLEDGE_BASE_SCHEMA = {
    'fact': str,                # The verified fact
    'source_report_id': str,    # Research report it came from
    'source_indices': [int],    # Source citations
    'confidence': str,          # 'high', 'medium', 'low'
    'category': str,            # 'person', 'event', 'location', 'general'
    'created_at': str
}

# Workflow phases
WORKFLOW_PHASES = [
    'research',
    'archive',
    'scripting',
    'interviews',
    'voiceover',
    'assembly',
    'review'
]
