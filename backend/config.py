import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    GCP_PROJECT = os.getenv('GCP_PROJECT', 'arrow-media-ai')
    GCS_BUCKET = os.getenv('GCS_BUCKET', 'aim-studio-uploads')
    GOOGLE_CLOUD_REGION = os.getenv('GOOGLE_CLOUD_REGION', 'us-central1')
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-prod')
    VERTEX_AI_LOCATION = os.getenv('VERTEX_AI_LOCATION', 'us-central1')
    DEBUG = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    PORT = int(os.getenv('PORT', 8080))
