from flask import Blueprint, jsonify
from utils.file_manager import load_json, append_json

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard", methods=["GET"])
def get_dashboard_stats():
    """Return aggregated dashboard statistics.

    Loads scan and event data from JSON files and returns counts
    required by the frontend dashboard.
    """
    scans = load_json("data/url_scans.json")
    events = load_json("data/security_events.json")

    total_scans = len(scans)
    safe = sum(1 for item in scans if item.get("status") == "SAFE")
    suspicious = sum(1 for item in scans if item.get("status") == "SUSPICIOUS")
    dangerous = sum(1 for item in scans if item.get("status") == "DANGEROUS")

    response = {
        "responseCode": "000",
        "responseMessage": "Success",
        "responseData": {
            "totalScans": total_scans,
            "safe": safe,
            "suspicious": suspicious,
            "dangerous": dangerous,
            "events": len(events),
        },
    }
    return jsonify(response)
