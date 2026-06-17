from flask import Blueprint, jsonify
from utils.file_manager import load_json

logs_bp = Blueprint("logs", __name__)


@logs_bp.route("/logs", methods=["GET"])
def get_logs():
    """Return all recorded security events.

    The frontend uses this endpoint to display and filter historic events.
    """
    events = load_json("backend/data/security_events.json")
    return (
        jsonify({
            "responseCode": "000",
            "responseMessage": "Success",
            "responseData": events,
        }),
        200,
    )
