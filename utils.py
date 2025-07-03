
import os
import hashlib
import json
from pathlib import Path

def ensure_dir(path):
    """Ensure directory exists."""
    os.makedirs(path, exist_ok=True)

def compute_sha256(filepath):
    """Compute SHA256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def save_json(data, filepath):
    """Save dictionary to JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def load_json(filepath):
    """Load JSON from a file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def get_project_root():
    """Get root directory of the project."""
    return Path(__file__).parent.parent.resolve()

def get_default_config_path():
    """Get default config file path."""
    return os.path.join(get_project_root(), "config.json")
