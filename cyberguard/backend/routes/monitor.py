from flask import Blueprint, jsonify
from utils.process_monitor import collect_process_data
from utils.file_manager import append_json
from utils.risk_calculator import build_event_item

monitor_bp = Blueprint("monitor", __name__)


@monitor_bp.route("/processes", methods=["GET"])
def get_processes():
    """Return a list of running processes and record any generated alerts.

    Calls the process collection utility which returns a tuple of
    (processes, alerts). Alerts are appended to the security events store.
    """
    processes, alerts = collect_process_data()

    for alert in alerts:
        append_json("backend/data/security_events.json", alert)

    return (
        jsonify({
            "responseCode": "000",
            "responseMessage": "Success",
            "responseData": processes,
        }),
        200,
    )
