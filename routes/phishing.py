from flask import Blueprint, request, jsonify
from utils.phishing_checker import analyze_url
from utils.file_manager import append_json, load_json
from utils.risk_calculator import build_event_item
from datetime import datetime

phishing_bp = Blueprint("phishing", __name__)


@phishing_bp.route("/scan", methods=["POST"])
def scan_url():
    """Endpoint to scan a provided URL and store the result.

    Expected JSON payload: {"url": "https://example.com"}
    The function analyzes the URL, persists the scan result to
    `data/url_scans.json`, and creates an event in
    `data/security_events.json` when the URL is flagged.
    """
    payload = request.get_json() or {}
    url = payload.get("url", "").strip()

    if not url:
        return (
            jsonify({
                "responseCode": "999",
                "responseMessage": "Invalid URL payload",
                "responseData": {},
            }),
            400,
        )

    scan_result = analyze_url(url)
    scan_result["scanDate"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    scan_result["id"] = scan_result.get("id")

    append_json("data/url_scans.json", scan_result)

    if scan_result["status"] in ["SUSPICIOUS", "DANGEROUS"]:
        event_item = build_event_item(
            event_type="PHISHING_ALERT",
            description=f"{scan_result['status']} URL detected: {url}",
            timestamp=scan_result["scanDate"],
        )
        append_json("data/security_events.json", event_item)

    return (
        jsonify({
            "responseCode": "000",
            "responseMessage": "Success",
            "responseData": scan_result,
        }),
        200,
    )
