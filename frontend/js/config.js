// Frontend configuration entrypoint.
// For local development default to the backend running on localhost:5000.
// Override by setting `window.API_BASE` in an inline script in HTML
// (must appear before this file is loaded) or by setting it externally.
// Example (production):
// <script>window.API_BASE = "https://your-backend.onrender.com/api";</script>

// Default to Render backend in production if not provided.
// Set to the provided Render app and include the API prefix.
window.API_BASE = window.API_BASE || "https://cybersecurity-2-n5mx.onrender.com/api";
