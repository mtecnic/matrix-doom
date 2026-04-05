"""Safe file reading and writing utilities."""

import json
import os
from pathlib import Path
from typing import Any, Optional


def read_text_file(path: str, default: str = "") -> str:
    """Read a text file safely, returning default if file doesn't exist."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except (OSError, IOError):
        return default


def read_json_file(path: str, default: Optional[Any] = None) -> Any:
    """Read a JSON file safely, returning default if file doesn't exist or is invalid."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, IOError, json.JSONDecodeError):
        return default if default is not None else {}


def write_text_file(path: str, content: str, mkdir: bool = True) -> bool:
    """Write text to a file safely, creating directories if needed."""
    try:
        if mkdir:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except (OSError, IOError):
        return False


def write_json_file(path: str, data: Any, mkdir: bool = True) -> bool:
    """Write data as JSON to a file safely, creating directories if needed."""
    try:
        if mkdir:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except (OSError, IOError, TypeError):
        return False


def ensure_directory(path: str) -> bool:
    """Ensure a directory exists, creating it if necessary."""
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except (OSError, IOError):
        return False


def file_exists(path: str) -> bool:
    """Check if a file exists."""
    return Path(path).is_file()


def get_file_size(path: str) -> int:
    """Get the size of a file in bytes, or 0 if it doesn't exist."""
    try:
        return Path(path).stat().st_size
    except (OSError, IOError):
        return 0
