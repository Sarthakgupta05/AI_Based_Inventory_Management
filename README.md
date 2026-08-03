# 📦 AI-Based Inventory Management & Demand Forecasting

An end-to-end time-series forecasting project built to predict product demand and optimize stock levels using classical statistical models, deep learning, and hybrid architectures.

---

## 📌 Problem Statement
In supply chain and inventory management, balancing stock levels is a critical challenge:
* **Overstocking:** Increases holding costs and locks up working capital.
* **Stockouts:** Results in missed market demand, lost revenue, and poor customer satisfaction.

This project benchmarks **6 distinct forecasting models** to accurately predict future demand, allowing for automated and data-driven inventory replenishment.

---

## 🏆 Performance Leaderboard

All models were trained and evaluated on historical demand trends using **Root Mean Squared Error (RMSE)**:

| Model | RMSE | Status / Notes |
| :--- | :---: | :--- |
| **ARIMA (5, 1, 0)** | **1222.30** | 🏆 **The Winner** |
| **Multivariate LSTM** | **1243.73** | 🥈 Close second |
| **LSTM (Univariate)** | **1244.49** | 🥉 Strong competitor |
| **SARIMAX** | **1273.62** | Baseline statistical model |
| **Prophet** | **1297.96** | Good for capturing seasonality |
| **Hybrid ARIMA-LSTM** | **7027.69** | Failed / Residual explosion |

---

## 💡 Key Insights

* **Classical Efficiency:** **ARIMA (5, 1, 0)** achieved the lowest error, showing that traditional statistical models can outperform deep learning architectures when strong linear autoregressive trends are present.
* **Neural Networks:** Both Multivariate and Univariate LSTMs delivered highly competitive results, effectively learning non-linear dependencies.
* **Hybrid Breakdown:** The Hybrid ARIMA-LSTM architecture suffered from error accumulation/residual explosion, causing a significant performance drop.

---

## 🛠️ Tech Stack & Dependencies

* **Language:** Python 3.x
* **Data Manipulation:** `pandas`, `numpy`
* **Classical Modeling:** `statsmodels`, `pmdarima`, `prophet`
* **Deep Learning:** `tensorflow` / `keras` or `torch`
* **Visualization:** `matplotlib`, `seaborn`

---
