<div align="center">

# 🌐 Network Traffic Congestion Predictor

An intelligent, ML-powered network monitoring dashboard that captures live packet flows, aggregates traffic throughput, and detects network congestion in real-time using a pre-trained **Random Forest** model.network flow analysis and congestion classification.

![Streamlit UI](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scapy](https://img.shields.io/badge/Scapy-000000?style=for-the-badge)
![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

</div>

---

## 💡 Overview
This application acts as a light-weight intrusion and throughput monitor. It captures local network packets in 2-second sampling windows, processes traffic features, and predicts whether the network is experiencing congestion or operating normally.
---

## Key Features
**Live Network Sniffing:** Uses scapy to continuously sniff active network traffic on selected interfaces (Wi-Fi, Ethernet, Hotspot).

**Private IP Filtering:** Filters traffic strictly within private local subnets (172.x.x.x, 192.168.x.x, 10.x.x.x) to eliminate public internet noise.

**ML-Based Congestion Inference:** Employs a pre-trained Random Forest Classifier to assess throughput parameters and assign a congestion confidence score.

**Dynamic, Flicker-Free UI:** Built with Streamlit's st.empty() container scaffolding to ensure real-time metric cards, active device lists, and line charts update seamlessly without UI flickering.


---
## 📊 Monitored Metrics

The dashboard evaluates traffic over rolling 2-second windows using four core features:

| Metric | Feature Description |
| :--- | :--- | 
| **Packets / Sec (PPS)** | Total network packets captured per second. | 
| **Total Bytes Captured** | Combined payload size of all packets in the sampling window.|
| **Avg Packet Size** | Mean packet byte size (Total Bytes / Total Packets) | 
| **Active Devices** | Total unique private IP addresses active during the sampling interval |

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