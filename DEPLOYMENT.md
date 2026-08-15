# Deployment Guide

This document shows how to deploy the Streamlit app for this repository.

## Quick: Streamlit Community Cloud (recommended)
1. Commit `app.py` to the repository root and ensure `requirements.txt` is present (Streamlit Cloud uses `requirements.txt`).
2. Go to https://streamlit.io/cloud and connect your GitHub account.
3. Create a new app and select this repository and branch (e.g., `main`).
4. Set the "Main file" to `app.py`.
5. Streamlit Cloud will automatically install dependencies from `requirements.txt`.
6. Deploy. The run command should be:
   `streamlit run app.py`

## Heroku (optional)
1. Make sure you have a `Procfile` in the repo root with the following content:
   `web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
2. Push the repo to a Heroku app (buildpacks for Python will be used). Heroku will use the Procfile to start the service on the assigned port.

## Docker (optional)
Create a Dockerfile that installs Python, copies repo, installs requirements, and runs:
```
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## Notes & fixes applied
- Added `requirements.txt` so Streamlit Community Cloud and other hosts can install dependencies reliably.
- Added `data/sample.csv` — a small example timeseries so the app can run without an uploaded CSV.
- Added `Procfile` to ensure platforms like Heroku start the app with Streamlit (avoids platforms defaulting to Uvicorn or other servers).
- The app already falls back to Python `pickle` when `joblib` is unavailable, and handles missing sample data gracefully.

## Next recommendations
- Pin exact versions in `requirements.txt` if you hit build failures (example: `streamlit==1.x.x`).
- If builds fail due to `pmdarima` (build time / binary compilation), consider training the model locally and committing `models/arima_model.pkl` for inference-only deployments.
- Optionally create a GitHub Actions workflow to run linting/tests on pull requests.
