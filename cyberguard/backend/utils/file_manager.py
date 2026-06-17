import json
import os
from threading import Lock

file_lock = Lock()


def ensure_file(path):
    """Ensure that the file and its parent directory exist.

    If the directory does not exist it will be created. If the file does not
    exist it is created and initialised with an empty JSON list to prevent
    subsequent JSON decode errors.

    Args:
        path (str): path to the JSON file to ensure
    """
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as file:
            json.dump([], file)


def load_json(path):
    """Load a JSON list from disk and return it.

    If the file is missing or corrupted an empty list is returned. This
    function guarantees a list is always returned for simplicity of callers.

    Args:
        path (str): Path to the JSON file

    Returns:
        list: parsed JSON list or []
    """
    abs_path = os.path.abspath(path)
    ensure_file(abs_path)
    try:
        with open(abs_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def save_json(path, data):
    """Persist a Python object (typically a list) as JSON to disk.

    Uses a file-level lock to avoid concurrent write corruption.

    Args:
        path (str): destination file path
        data (any): JSON serializable Python object
    """
    abs_path = os.path.abspath(path)
    ensure_file(abs_path)
    try:
        with file_lock:
            with open(abs_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2)
    except IOError:
        # In case of write failure, swallow error to let the application
        # continue; callers may choose to validate persisted state.
        pass


def append_json(path, item):
    """Append an item to a JSON list stored on disk.

    This function reads the current list, appends the new item and writes
    the data back. It ensures files are created if missing.

    Args:
        path (str): path to JSON file
        item (dict): item to append
    """
    abs_path = os.path.abspath(path)
    ensure_file(abs_path)
    current_data = load_json(abs_path)
    current_data.append(item)
    save_json(abs_path, current_data)
