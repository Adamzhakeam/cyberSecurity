# CyberGuard Security Suite

Lightweight cybersecurity monitoring platform (Flask backend + static frontend).

## Features

- URL phishing scanner with rule-based risk scoring
- Process monitor using `psutil`
- Security events stored in JSON files
- Dashboard with basic charts (pure JS canvas)

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

Start the backend server:

```bash
cd '/home/predator/Documents/practice/cyberSecurity project /cyberguard/backend'
python app.py
```

Open the UI at: `http://localhost:5000`

## File storage

All data is persisted as JSON under `backend/data/`:

- `url_scans.json` — saved URL scan results
- `security_events.json` — security events and alerts
- `system_stats.json` — reserved for future use

## Notes

- This project is defensive only. It performs local analysis and stores results in JSON files.
- If files do not exist, the app will create them automatically.

## Development

- Backend: Python + Flask
- Frontend: static HTML/CSS/JS in `frontend/`

## License

MIT (use as you like)
