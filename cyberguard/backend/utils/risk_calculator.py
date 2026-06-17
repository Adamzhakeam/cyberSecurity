from datetime import datetime
from utils.file_manager import load_json


def load_next_id(path, prefix):
    """Generate the next sequential ID for items stored in a JSON list.

    Scans existing items and returns a new identifier with the provided
    prefix and zero-padded numeric suffix (e.g. URL001, EVT002).

    Args:
        path (str): path to JSON file containing existing items
        prefix (str): textual prefix for the ID

    Returns:
        str: new unique identifier
    """
    items = load_json(path)
    if not items:
        return f"{prefix}001"

    highest = 0
    for item in items:
        item_id = item.get("id") or item.get("eventId")
        if isinstance(item_id, str) and item_id.startswith(prefix):
            try:
                value = int(item_id.replace(prefix, ""))
                highest = max(highest, value)
            except ValueError:
                continue
    return f"{prefix}{highest + 1:03d}"


def build_scan_item(url, score, status, reasons):
    """Construct a scan record compatible with storage format.

    Args:
        url (str): normalized URL
        score (int): risk score
        status (str): classification
        reasons (list): list of reason strings

    Returns:
        dict: scan record
    """
    next_id = load_next_id("backend/data/url_scans.json", "URL")
    return {
        "id": next_id,
        "url": url,
        "riskScore": score,
        "status": status,
        "reasons": reasons,
    }


def build_event_item(event_type, description, timestamp=None):
    """Create a security event record with a unique ID.

    Args:
        event_type (str): short event type key (eg. PHISHING_ALERT)
        description (str): human readable description
        timestamp (str|None): optional timestamp string

    Returns:
        dict: event record
    """
    next_event_id = load_next_id("backend/data/security_events.json", "EVT")
    return {
        "eventId": next_event_id,
        "eventType": event_type,
        "description": description,
        "timestamp": timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
