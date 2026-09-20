<div align="center">

# 🌐 Network Traffic Congestion Predictor

**An end-to-end Machine Learning pipeline for real-time network flow analysis and congestion classification.**

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3-orange?style=for-the-badge&logo=scikitlearn)
![Accuracy](https://img.shields.io/badge/Accuracy-99.94%25-success?style=for-the-badge)

</div>

---

## 📌 Features

- ⚡ **Real-Time Classification:** Instantly classifies network flows as `NORMAL` or `CONGESTED`.
- 📊 **Explainable AI:** Feature importance scoring highlights key network drivers (Packets Per Second).
- 💻 **Interactive CLI:** Live terminal interface for manual parameter testing.
- 💾 **Model Serialization:** Reusable binary weights exported via `joblib`.

---

## 📊 Feature Importance Breakdown

| Network Metric | Importance Score | Impact |
| :--- | :--- | :--- |
| **Packets per Second (PPS)** | `0.570` | Primary Congestion Driver (~57%) |
| **Packet Size** | `0.197` | Secondary Factor (~20%) |
| **Traffic Volume (Bytes)** | `0.127` | Moderate Impact (~13%) |
| **Flow Duration** | `0.106` | Minimal Impact (~10%) |

---

## 📁 Repository Structure
```
D:\ML

├── preprocessed_dataset.csv   # Network traffic dataset
├── train_model.py            # Model training &serialization
├── congestion_model.pkl      # Saved Random Forest model
├── predict.py                 # Static test predictions script
├── check_importance.py        # Feature importance inspector
├── interactive_predict.py     # Interactive CLI tool
└── README.md                  # Project documentation
``` 
---

## 🛠️ Requirements & Installation

### Prerequisites
* **Python:** Version 3.10 or higher
* **OS:** Windows 11 / Linux / macOS

### Required Packages
Install all necessary dependencies via `pip`:

```bash
pip install pandas scikit-learn joblib

```
---

## 🚀 How to Run

### 1. Run Interactive Prediction Tool (CLI)
Test custom telemetry inputs manually with instant feedback and probability scoring:
```bash
python interactive_predict.py
```
### 2. Inspect Feature Importance
Evaluate how much each network metric impacts the decision tree calculations:

```Bash
python check_importance.py
```
### 3. Run Static Automated Tests
Execute predefined synthetic test scenarios against the serialized binary model:

```Bash
python predict.py
```
### 4. Retrain the Pipeline
Train the Random Forest classifier from scratch and regenerate congestion_model.pkl:

```Bash
python train_model.py
```
---

## 💡 Engineering Workflow

1. **Data Ingestion:** Loaded network flow metrics from `preprocessed_dataset.csv`.
2. **Feature Engineering:** Mapped target label `is_congested` dynamically using `Bandwidth Utilization > 0.70`.
3. **Model Selection:** Trained `RandomForestClassifier(n_estimators=100)`.
4. **Serialization:** Saved trained pipeline weights into `congestion_model.pkl` using `joblib` for zero-latency loading.
5. **CLI Deployment:** Implemented error-handled user input parser for real-time terminal inference.