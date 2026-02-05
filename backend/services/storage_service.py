"""Google Cloud Storage service."""
import os
import hashlib
from google.cloud import storage
from config import Config

storage_client = storage.Client()
bucket = storage_client.bucket(Config.GCS_BUCKET)


def upload_file(file_obj, destination_path):
    """
    Upload a file to GCS.

    Args:
        file_obj: File-like object to upload
        destination_path: Path in the bucket (e.g., 'uploads/project-id/filename.pdf')

    Returns:
        dict with url and metadata
    """
    blob = bucket.blob(destination_path)

    # Read content for hash
    content = file_obj.read()
    file_hash = hashlib.md5(content).hexdigest()
    file_obj.seek(0)

    # Upload
    blob.upload_from_file(file_obj)

    # Make publicly readable (or use signed URLs for private access)
    blob.make_public()

    return {
        'url': blob.public_url,
        'path': destination_path,
        'hash': file_hash,
        'size': len(content),
        'content_type': blob.content_type
    }


def get_signed_url(path, expiration=3600):
    """
    Get a signed URL for private file access.

    Args:
        path: Path to the file in the bucket
        expiration: URL expiration time in seconds

    Returns:
        Signed URL string
    """
    blob = bucket.blob(path)
    return blob.generate_signed_url(expiration=expiration)


def delete_file(path):
    """Delete a file from GCS."""
    blob = bucket.blob(path)
    blob.delete()


def list_files(prefix):
    """List files with a given prefix."""
    blobs = bucket.list_blobs(prefix=prefix)
    return [{'name': blob.name, 'size': blob.size, 'updated': blob.updated} for blob in blobs]
