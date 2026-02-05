"""Vertex AI service for deep research."""
import json
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from config import Config

# Initialize Vertex AI
vertexai.init(project=Config.GCP_PROJECT, location=Config.VERTEX_AI_LOCATION)

# Use Gemini 2.0 Flash
model = GenerativeModel("gemini-2.0-flash-exp")

RESEARCH_SYSTEM_PROMPT = """You are AiM, an AI research assistant for documentary production.

You perform deep research to help documentary producers gather verified facts, identify key people, and build comprehensive knowledge bases for their episodes.

Output format (respond in valid JSON only, no markdown code blocks):
{
  "executive_summary": "Dense narrative paragraph with [n] source indices referencing your sources...",
  "key_findings": [
    {
      "name": "Person or fact name",
      "description": "Detailed description with relevant context",
      "source_indices": [1, 2],
      "confidence": "high|medium|low"
    }
  ],
  "bibliography": {
    "ai_generated": ["Source 1 description", "Source 2 description"],
    "external": ["URL or reference 1", "URL or reference 2"]
  }
}

Rules:
- Every fact must have a confidence level (high/medium/low) and source indices
- Cross-reference against the existing knowledge base to avoid duplication
- If an attached file doesn't match the query, say so honestly in the executive summary
- Be thorough: aim for 10+ key findings per research query when possible
- Source indices [n] in the executive summary should correspond to the bibliography entries
- Never fabricate sources - if you cannot verify something, mark confidence as low
- Focus on documentary-relevant information: people, events, dates, locations, controversies, lesser-known facts"""


def deep_research(query, series_title, episode_title, episode_brief, existing_kb, attached_files=None):
    """
    Perform deep research using Vertex AI.

    Args:
        query: The research query from the producer
        series_title: Title of the series
        episode_title: Title of the episode
        episode_brief: Episode brief/description
        existing_kb: List of existing knowledge base entries
        attached_files: Optional list of attached file URLs/paths

    Returns:
        dict with executive_summary, key_findings, and bibliography
    """
    # Build context
    kb_summary = ""
    if existing_kb:
        kb_facts = [entry.get('fact', '') for entry in existing_kb[:20]]  # Limit to 20 entries
        kb_summary = "Existing verified facts:\n" + "\n".join(f"- {fact}" for fact in kb_facts)

    prompt = f"""Context:
- Series: {series_title}
- Episode: {episode_title}
- Episode Brief: {episode_brief}

{kb_summary}

Research Query: {query}

Perform comprehensive deep research on this query. Gather verified facts, identify key people and events, and provide source citations. Remember to output valid JSON only."""

    try:
        # Build content parts
        contents = [prompt]

        # Add attached files if any (for multimodal)
        if attached_files:
            for file_info in attached_files:
                if isinstance(file_info, dict) and 'url' in file_info:
                    # For now, mention the file in the prompt
                    contents[0] += f"\n\nAttached file for analysis: {file_info.get('name', 'Unknown file')}"

        response = model.generate_content(
            contents,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 4096,
            }
        )

        # Parse JSON response
        response_text = response.text.strip()

        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]

        result = json.loads(response_text.strip())

        return {
            'executive_summary': result.get('executive_summary', ''),
            'key_findings': result.get('key_findings', []),
            'bibliography': result.get('bibliography', {'ai_generated': [], 'external': []})
        }

    except json.JSONDecodeError as e:
        # If JSON parsing fails, return a basic structure with the raw response
        return {
            'executive_summary': f"Research completed but response parsing failed. Raw response available.",
            'key_findings': [{
                'name': 'Parse Error',
                'description': str(e),
                'source_indices': [],
                'confidence': 'low'
            }],
            'bibliography': {'ai_generated': [], 'external': []}
        }
    except Exception as e:
        return {
            'executive_summary': f"Research failed: {str(e)}",
            'key_findings': [],
            'bibliography': {'ai_generated': [], 'external': []}
        }
