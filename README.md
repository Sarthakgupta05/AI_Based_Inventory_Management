# 📦 AI-Based Inventory Management System

Demand forecasting and intelligent reordering using time-series and deep-learning models.

This project predicts short-term product demand from two years of daily retail sales data and turns those forecasts directly into actionable inventory decisions — reorder points, low-stock alerts, a what-if pricing simulator, and automated purchase orders.

## Overview

Retail inventory decisions are usually reactive: static reorder thresholds that ignore seasonality, pricing, and promotions, leading to stockouts on one end and overstocking on the other. This project builds a full pipeline that:

1. Forecasts near-term demand using multiple models
2. Selects the best-performing forecaster
3. Converts that forecast into a Reorder Point (ROP) and safety-stock buffer
4. Automatically raises low-stock alerts and drafts purchase orders
5. Lets planners simulate "what-if" pricing/discount scenarios

## Dataset

| | |
|---|---|
| Rows | 73,100 daily store-product records |
| Columns | 15 |
| Date range | Jan 1, 2022 – Jan 1, 2024 |
| Missing values | None |

Key fields: `Date`, `Store ID`, `Product ID`, `Category`, `Region`, `Inventory Level`, `Units Sold`, `Units Ordered`, `Demand Forecast`, `Price`, `Discount`, `Weather Condition`, `Holiday/Promotion`, `Competitor Pricing`, `Seasonality`.

## Models Evaluated

Six forecasting approaches were trained and back-tested on the same 30-day held-out window, ranked by RMSE:

| Model | RMSE | Verdict |
|---|---|---|
| **ARIMA (5,1,0)** | **1,222.30** | **Best model — lowest error** |
| Multivariate LSTM | 1,243.73 | Close second |
| LSTM (Univariate) | 1,244.49 | Strong competitor |
| SARIMAX | 1,273.62 | Slightly worse |
| Prophet | 1,297.96 | Good for seasonality |
| Hybrid ARIMA-LSTM | 7,027.69 | Failed / diverged |

ARIMA(5,1,0) was selected as the production forecaster: lowest error, simplest model, and fastest to retrain.

## Inventory Logic

```
Reorder Point = (Average Daily Demand × Lead Time) + Safety Stock
```

The winning forecast feeds:
- **Reorder Point engine** — computes when to reorder per product
- **Low-stock alerts** — flags products projected to fall below threshold
- **What-if simulator** — `what_if_inventory_analysis(new_discount_level, new_price)` projects demand under a hypothetical pricing scenario
- **Purchase order automation** — drafts and saves a CSV purchase order when demand exceeds available stock plus safety buffer


## Tech Stack

- **Language:** Python 3
- **Data handling:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Statistical forecasting:** Statsmodels (ARIMA, SARIMAX), Prophet
- **Machine learning:** Scikit-learn, XGBoost
- **Deep learning:** TensorFlow / Keras (LSTM)
- **Environment:** Jupyter Notebook

## Getting Started

### Prerequisites

```bash
pip install numpy pandas matplotlib seaborn scikit-learn statsmodels prophet xgboost tensorflow
```

### Run the notebook

```bash
jupyter notebook AI_Based_Inventory_Management.ipynb
```

Run all cells top to bottom — the notebook loads the dataset, runs EDA, trains and compares all six models, then generates the reorder point, alerts, and purchase order examples.

## Results Summary

- ARIMA(5,1,0) achieved the best test-set accuracy among all six models compared.
- Deep-learning models (LSTM variants) were competitive but did not outperform the tuned classical baseline.
- The hybrid ARIMA-LSTM residual experiment is documented as a negative result — stacking an LSTM on ARIMA's residuals increased error rather than reducing it.
- Forecasts were successfully translated into automated reorder points, alerts, and draft purchase orders, closing the loop from prediction to action.

## Future Scope

- Product-level (SKU × store) forecasting instead of aggregated totals
- Real-time retraining pipeline and a live planner-facing dashboard
- Multi-echelon inventory optimization across warehouses and stores
- Incorporate supplier lead-time variability into safety-stock sizing
- Scheduled service to auto-send low-stock alerts and draft POs to procurement

## Team

| Role | Name |
|---|---|
| [ Add team member ] | [ Add role ] |
| [ Add team member ] | [ Add role ] |

## License

[ Add license — e.g. MIT ]
* **Classical Modeling:** `statsmodels`, `pmdarima`, `prophet`
* **Deep Learning:** `tensorflow` / `keras` or `torch`
* **Visualization:** `matplotlib`, `seaborn`

---
