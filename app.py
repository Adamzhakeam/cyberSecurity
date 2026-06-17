from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from routes.dashboard import dashboard_bp
from routes.phishing import phishing_bp
from routes.monitor import monitor_bp
from routes.logs import logs_bp
import os

# Dynamically configure the frontend static folder only when present.
# This lets the backend be deployed separately on Render without the
# static frontend included in the same repo.
base_dir = os.path.dirname(os.path.abspath(__file__))
# When running from project root the frontend folder sits next to this file.
frontend_path = os.path.abspath(os.path.join(base_dir, "frontend"))
if os.path.exists(frontend_path):
    app = Flask(__name__, static_folder=frontend_path, template_folder=frontend_path)
else:
    app = Flask(__name__)
CORS(app)

app.register_blueprint(dashboard_bp, url_prefix="/api")
app.register_blueprint(phishing_bp, url_prefix="/api/phishing")
app.register_blueprint(monitor_bp, url_prefix="/api")
app.register_blueprint(logs_bp, url_prefix="/api")


@app.route("/", methods=["GET"])
def serve_index():
    """Serve the main index page.

    Returns the `index.html` file from the frontend static folder.
    """
    if app.static_folder and os.path.exists(os.path.join(app.static_folder, "index.html")):
        return send_from_directory(app.static_folder, "index.html")
    # No frontend bundled with this deployment — return a simple API status.
    return jsonify({
        "responseCode": "000",
        "responseMessage": "API Running",
        "responseData": {},
    })


@app.route("/<path:path>", methods=["GET"])
def serve_frontend(path):
    """Serve static frontend files.

    If the requested frontend asset exists in the configured static folder,
    return it. Otherwise return `index.html` to support client-side routing.

    Args:
        path (str): relative path requested by the browser
    """
    if app.static_folder and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    # If there's a frontend present serve index to support client routing,
    # otherwise return a standardized JSON response.
    if app.static_folder and os.path.exists(os.path.join(app.static_folder, "index.html")):
        return send_from_directory(app.static_folder, "index.html")
    return (
        jsonify({
            "responseCode": "999",
            "responseMessage": "Frontend not available on this backend deployment",
            "responseData": {},
        }),
        404,
    )


@app.errorhandler(404)
def page_not_found(error):
    """Return a JSON formatted 404 response.

    This keeps API responses standardized when a resource is not found.
    """
    return (
        jsonify({
            "responseCode": "999",
            "responseMessage": "Resource not found",
            "responseData": {},
        }),
        404,
    )


if __name__ == "__main__":
    # Use environment variables so Render can set the PORT and debug mode.
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") in ("1", "true", "True")
    app.run(host="0.0.0.0", port=port, debug=debug)
