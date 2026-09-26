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

## 🏗️ System Architecture
```text
[ Connected Devices ]
    (Laptop / Phones)
           │
           ▼
 [ Network Interface ] (Wi-Fi / Ethernet)
           │
           ▼
 [ Scapy Sniffer ] ───> 2-Second Sampling Window
                               │
                               ▼
                   [ Local IP & Feature Extractor ]
                               │
                               ▼
                   [ Random Forest Model ]
                               │
                               ▼
                   [ Streamlit Dynamic UI ]

```
## 📁 Repository Structure
```
D:\ML


├── app.py                     # Main Streamlit dashboard & Scapy packet pipeline
├── train_model.py             # Model training & serialization script
├── preprocessed_dataset.csv   # Network traffic dataset used for ML model
├── congestion_model.pkl       # Pre-trained Random Forest model
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
``` 
---

## 🛠️ Requirements & Installation

### Prerequisites
* **Python:** Version 3.10 or higher
* **OS:** Windows 11 / Linux / macOS

## Installation
1. **Clone the repository**
```
git clone [https://github.com/Srivarsha-puppala/NetPulse.git](https://github.com/Srivarsha-puppala/NetPulse.git)
cd NetPulse
```
2. **Dependencies**

Install all necessary dependencies via pip:

```

pip install streamlit scapy pandas scikit-learn joblib
```



---

## 🚀 How to Run
Run the live ML-powered Streamlit web interface:
```
streamlit run app.py
```
ensure your VS Code terminal or Command Prompt is opened with "Run as Administrator" so scapy can capture Wi-Fi packets without permission errors.

## 💡 Engineering Workflow

1. **Data Ingestion:** Loaded network flow metrics from `preprocessed_dataset.csv`.
2. **Feature Engineering:** Mapped target label `is_congested` dynamically using `Bandwidth Utilization > 0.70`.
3. **Model Selection:** Trained `RandomForestClassifier(n_estimators=100)`.
4. **Serialization:** Saved trained pipeline weights into `congestion_model.pkl` using `joblib` for zero-latency loading.
5. **CLI Deployment:** Implemented error-handled user input parser for real-time terminal inference.