from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from routes.dashboard import dashboard_bp
from routes.phishing import phishing_bp
from routes.monitor import monitor_bp
from routes.logs import logs_bp
import os

app = Flask(__name__, static_folder="../frontend", template_folder="../frontend")
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
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>", methods=["GET"])
def serve_frontend(path):
    """Serve static frontend files.

    If the requested frontend asset exists in the configured static folder,
    return it. Otherwise return `index.html` to support client-side routing.

    Args:
        path (str): relative path requested by the browser
    """
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


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
    app.run(host="0.0.0.0", port=5000, debug=True)
