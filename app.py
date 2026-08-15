"""
Streamlit app for AI_Based_Inventory_Management
- Load a CSV of historical demand or use an existing saved ARIMA/SARIMA model
- Fit a simple ARIMA model (if pmdarima available) or load model file models/arima_model.pkl
- Produce a forecast and basic plots

Usage:
  pip install -r requirements-ext.txt
  streamlit run app.py
"""
import os
import io
import pickle
try:
    import joblib
except ModuleNotFoundError:
    # joblib not installed in the environment (Streamlit Cloud sometimes omits optional deps).
    # Fall back to Python's pickle for loading/saving model files so the app doesn't crash on import.
    joblib = None
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Inventory Forecasting (ARIMA/SARIMA)", layout="centered")

st.title("Inventory Demand Forecasting")
st.markdown(
    "This app runs a simple ARIMA/SARIMA forecasting flow. You can upload a CSV with a datetime column and a demand column, "
    "or load a pre-trained model from models/arima_model.pkl if present."
)

# Sidebar controls
st.sidebar.header("Options")
uploaded_file = st.sidebar.file_uploader("Upload CSV (time series)", type=["csv"])
use_sample = st.sidebar.checkbox("Use sample file in repo (data/sample.csv)", value=False)
date_col = st.sidebar.text_input("Datetime column name (if any)", value="date")
value_col = st.sidebar.text_input("Value column name (demand)", value="demand")
freq = st.sidebar.selectbox("Resample frequency (optional)", ["None", "D", "W", "M"], index=0)
forecast_periods = st.sidebar.number_input("Forecast periods (steps)", min_value=1, max_value=365, value=30)
fit_model_now = st.sidebar.button("Fit ARIMA now (may take time)")

# Helper to read csv from uploaded or repo path
@st.cache_data
def load_csv_from_bytes(bytes_data):
    return pd.read_csv(io.BytesIO(bytes_data))

def load_csv_from_path(path):
    return pd.read_csv(path)

def ensure_datetime_index(df, date_col):
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.set_index(date_col).sort_index()
    elif isinstance(df.index, pd.DatetimeIndex):
        pass
    else:
        st.error("No datetime column found and index is not datetime. Please provide a datetime column.")
        return None
    return df

# Load data
df = None
if uploaded_file is not None:
    try:
        raw = uploaded_file.read()
        df = load_csv_from_bytes(raw)
    except Exception as e:
        st.error(f"Failed to read uploaded CSV: {e}")
elif use_sample:
    sample_path = "data/sample.csv"
    if os.path.exists(sample_path):
        df = load_csv_from_path(sample_path)
    else:
        st.warning("No sample file found at data/sample.csv in repo.")
else:
    st.info("Upload a CSV or check 'Use sample file in repo' to begin.")

if df is not None:
    st.subheader("Loaded data (first rows)")
    st.dataframe(df.head())
    df2 = ensure_datetime_index(df.copy(), date_col)
    if df2 is None:
        st.stop()
    if value_col not in df2.columns:
        st.error(f"Value column '{value_col}' not found in data.")
        st.stop()
    series = df2[value_col].astype(float)

    # Optional resample
    if freq != "None":
        series = series.resample(freq).sum()
        st.write(f"Resampled to frequency: {freq}")

    st.line_chart(series)

    # Try to load an existing model if present
    model_path = "models/arima_model.pkl"
    model = None
    if os.path.exists(model_path):
        try:
            if joblib is not None:
                model = joblib.load(model_path)
            else:
                # fallback to pickle when joblib isn't available
                with open(model_path, "rb") as f:
                    model = pickle.load(f)
            st.success(f"Loaded model from {model_path}")
        except Exception as e:
            st.warning(f"Failed to load existing model: {e}")

    # Forecast using loaded model
    if model is not None:
        try:
            forecast = model.predict(n_periods=int(forecast_periods))
            index = pd.date_range(start=series.index[-1], periods=int(forecast_periods) + 1, closed="right", freq=getattr(series.index, "freq", None) or pd.infer_freq(series.index) or "D")
            forecast_series = pd.Series(forecast, index=index)
            st.subheader("Forecast from saved model")
            st.line_chart(pd.concat([series, forecast_series.rename("forecast")], axis=1))
        except Exception as e:
            st.error(f"Failed to forecast with loaded model: {e}")

    # Fit a model now using pmdarima (if available) when user requests
    if fit_model_now:
        st.info("Fitting ARIMA model (using pmdarima.auto_arima if available). This can take several minutes.")
        try:
            import pmdarima as pm
            with st.spinner("Running auto_arima..."):
                arima_model = pm.auto_arima(series.dropna(), seasonal=False, stepwise=True, suppress_warnings=True)
            st.success("ARIMA model fitted.")
            # Save model for reuse
            os.makedirs("models", exist_ok=True)
            if joblib is not None:
                joblib.dump(arima_model, "models/arima_model.pkl")
            else:
                # fallback to pickle when joblib isn't available
                with open("models/arima_model.pkl", "wb") as f:
                    pickle.dump(arima_model, f)
            st.write("Saved model to models/arima_model.pkl")
            # Forecast
            fcast = arima_model.predict(n_periods=int(forecast_periods))
            idx = pd.date_range(start=series.index[-1], periods=int(forecast_periods) + 1, closed="right", freq=getattr(series.index, "freq", None) or pd.infer_freq(series.index) or "D")
            fseries = pd.Series(fcast, index=idx)
            st.subheader("Forecast (auto_arima)")
            st.line_chart(pd.concat([series, fseries.rename("forecast")], axis=1))
        except ModuleNotFoundError:
            st.error("pmdarima is not installed in the environment. Install it or load a saved model.")
        except Exception as e:
            st.error(f"Model fitting failed: {e}")

    st.markdown("---")
    st.markdown("Tip: If you have a pre-trained model, place it at models/arima_model.pkl (joblib/pickle) and reload this app.")
else:
    st.stop()

st.markdown("## Notes")
st.markdown(
    "- This app is intentionally small and generic. Adapt the fitting/forecasting logic to use SARIMA parameters, exogenous variables, or your repo's notebooks as needed.\n"
    "- The repository contains Jupyter Notebooks — consider exporting the final trained model and placing it in models/ for fast inference."
)
