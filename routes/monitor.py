from flask import Blueprint, jsonify
from utils.process_monitor import collect_process_data
from utils.file_manager import append_json, load_json
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
        append_json("data/security_events.json", alert)

    return (
        jsonify({
            "responseCode": "000",
            "responseMessage": "Success",
            "responseData": processes,
        }),
        200,
    )


@monitor_bp.route("/alerts", methods=["GET"])
def get_alerts():
    """Return stored security events (alerts).

    This endpoint exposes the persisted security events so the frontend
    can fetch and display alert notifications.
    """
    events = load_json("data/security_events.json")
    return (
        jsonify({
            "responseCode": "000",
            "responseMessage": "Success",
            "responseData": events,
        }),
        200,
    )
