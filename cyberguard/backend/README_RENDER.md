Render deployment notes
----------------------

1. The backend entrypoint is `app.py` inside this folder.
2. This repo includes `Procfile` which runs:

   `gunicorn app:app --bind 0.0.0.0:$PORT`

3. Install dependencies from `requirements.txt` and the service will start.
4. The backend no longer requires the frontend to be present. If the
   frontend is bundled, it will be served; otherwise the root `/` will
   return a simple API status JSON response.
