# Deployment Guide

This document shows how to deploy the Streamlit app for this repository.

## Quick: Streamlit Community Cloud (recommended)
1. Commit `app.py` to the repository root and ensure `requirements-ext.txt` is present.
2. Go to https://streamlit.io/cloud and connect your GitHub account.
3. Create a new app and select this repository and branch (e.g., `add-streamlit-app` or `main`).
4. Set the "Main file" to `app.py`.
5. In "Advanced settings" -> "Install dependencies", you can put:
   - `pip install -r requirements-ext.txt`
   or leave Streamlit to auto-install if you included `requirements.txt`.
6. Deploy. The run command should be:
   `streamlit run app.py`

## Docker (optional)
Create a Dockerfile that installs Python, copies repo, installs requirements, and runs:
```
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## Notes
- The repo currently contains Jupyter Notebooks as the primary code artifacts. For production, export your trained models (e.g., using `joblib.dump`) to `models/arima_model.pkl` so the app can load them for fast inference.
- If your forecasting uses heavier dependencies (e.g., specific versions), pin them in `requirements-ext.txt` or add a `requirements.txt`.
