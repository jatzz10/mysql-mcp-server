"""
Utility helper functions for MySQL MCP Server
"""

import json
import hashlib
import os
from pathlib import Path
from typing import Any, Dict, Optional

def save_json_file(data: Dict[str, Any], file_path: str) -> None:
    """Save data to JSON file atomically"""
    try:
        # Write to temporary file first
        temp_file = f"{file_path}.tmp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        
        # Atomic move
        Path(temp_file).rename(file_path)
        
    except Exception as e:
        raise Exception(f"Error saving JSON file: {e}")

def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """Load data from JSON file"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    except Exception as e:
        raise Exception(f"Error loading JSON file: {e}")

def create_hash(text: str) -> str:
    """Create MD5 hash of text"""
    return hashlib.md5(text.encode()).hexdigest()
