import os
import time
import ipaddress
import pandas as pd
import numpy as np
import streamlit as st
import joblib
from scapy.all import sniff
from scapy.layers.inet import IP

# ---------------------------------------------------------
# Page Configuration & UI Layout
# ---------------------------------------------------------
st.set_page_config(
    page_title="Real-Time Network Congestion Detector",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Real-Time Network Congestion Detector")
st.caption("ML-Based Prediction using Live Traffic Flow Parameters & Multi-Device Monitoring")

# Load Trained ML Model (Robust Directory Path Fix)
@st.cache_resource
def load_model():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "congestion_model.pkl")
        model = joblib.load(model_path)
        return model
    except Exception as e:
        st.error(f"Failed to load model.pkl: {e}")
        return None

model = load_model()

if model:
    st.success("Random Forest Model Loaded Successfully!")

# ---------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------
st.sidebar.header("🕹️ Control Panel")

# Interface selection
selected_iface = st.sidebar.selectbox(
    "Select Active Network Interface",
    ["Wi-Fi", "Ethernet", "wlan0", "eth0"],
    index=0
)

run_monitoring = st.sidebar.checkbox("🔴 Start Live Network Sniffing", value=False)
sample_interval = st.sidebar.slider("Sampling Window (Seconds)", min_value=1, max_value=5, value=2)

# ---------------------------------------------------------
# Scapy Live Packet Aggregator
# ---------------------------------------------------------
class PacketAggregator:
    def __init__(self):
        self.packet_count = 0
        self.total_bytes = 0
        self.active_devices = set()

    def process_packet(self, packet):
        self.packet_count += 1
        self.total_bytes += len(packet)

        # Count each active device by its unique local IP address.
        if packet.haslayer(IP):
            source_ip = ipaddress.ip_address(packet[IP].src)
            if (source_ip.is_private and not source_ip.is_loopback
                    and not source_ip.is_multicast and not source_ip.is_unspecified):
                self.active_devices.add(str(source_ip))

    def get_metrics(self):
        metrics = {
            "Packets per Second (PPS)": self.packet_count / sample_interval,
            "Traffic Volume (Bytes)": self.total_bytes,
            "Avg Packet Size": (self.total_bytes / self.packet_count) if self.packet_count > 0 else 0,
            "Device Count": len(self.active_devices),
            "Active Devices": list(self.active_devices)
        }
        # Reset window frame state
        self.packet_count = 0
        self.total_bytes = 0
        self.active_devices = set()
        return metrics

# ---------------------------------------------------------
# Dashboard Metric Cards & Layout Holders
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
metric_pps = col1.empty()
metric_bytes = col2.empty()
metric_size = col3.empty()
metric_devices = col4.empty()

status_box = st.empty()
device_box = st.empty()
chart_box = st.empty()

# Initialize session state for rolling charts
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(
        columns=['Time', 'Raw PPS', 'Smoothed PPS', 'Congestion Probability (%)']
    )

# ---------------------------------------------------------
# Execution Loop
# ---------------------------------------------------------
if run_monitoring:
    aggregator = PacketAggregator()
    st.toast(f"Sniffing on interface: {selected_iface} (Promiscuous Mode Active)")

    while run_monitoring:
        # Sniff packets live in promiscuous mode
        try:
            sniff(
                iface=selected_iface,
                prn=aggregator.process_packet,
                timeout=sample_interval,
                store=False,
                promisc=True  # Enables capturing multi-device ambient frames
            )
        except Exception as err:
            st.error(f"Sniffing error on {selected_iface}: {err}")
            break

        # Extract metrics for current window
        data = aggregator.get_metrics()
        current_time = time.strftime("%H:%M:%S")

        # 1. Update UI KPI Metric Cards
        metric_pps.metric("Packets / Sec (PPS)", f"{data['Packets per Second (PPS)']:.1f}")
        metric_bytes.metric("Total Bytes Captured", f"{data['Traffic Volume (Bytes)']} B")
        metric_size.metric("Avg Packet Size", f"{data['Avg Packet Size']:.1f} B")
        metric_devices.metric("Active Devices", f"{data['Device Count']}")

        # 2. Render Active Device IPs
        with device_box.container():
            with st.expander("📲 Active Devices Captured in Last Window", expanded=True):
                if data["Active Devices"]:
                    st.write("Local IP addresses active on the network:")
                    st.code(", ".join(data["Active Devices"]), language="text")
                else:
                    st.write("No active device traffic detected in this interval.")

        # 3. Calculate 3-Sample Rolling Moving Average
        raw_pps = data['Packets per Second (PPS)']
        
        # Pull past raw PPS values to smooth jitter
        past_pps = st.session_state.history['Raw PPS'].tail(2).tolist()
        past_pps.append(raw_pps)
        smoothed_pps = float(np.mean(past_pps))

        # 4. Perform ML Prediction
        # Features: [PPS, Total Bytes, Avg Packet Size]
        #features = np.array([[smoothed_pps, data['Traffic Volume (Bytes)'], data['Avg Packet Size']]])
        # Updated line (4 features)
        features = np.array([[smoothed_pps, data['Traffic Volume (Bytes)'], data['Avg Packet Size'], data['Device Count']]])
        if model:
            prediction = model.predict(features)[0]
            probabilities = model.predict_proba(features)[0]
            congestion_prob = probabilities[1] * 100 if len(probabilities) > 1 else (100.0 if prediction == 1 else 0.0)

            if prediction == 1 or congestion_prob > 50.0:
                status_box.error(f"🚨 CONGESTED NETWORK DETECTED | Model Confidence: {congestion_prob:.2f}%")
            else:
                status_box.success(f"✅ NORMAL NETWORK OPERATION | Model Confidence: {100 - congestion_prob:.2f}%")
        else:
            congestion_prob = 0.0
            status_box.info("Running in Data Aggregation Mode (No ML Model Loaded)")

        # 5. Append Record to Rolling History (Keep Last 20 Samples)
        new_row = pd.DataFrame([{
            'Time': current_time,
            'Raw PPS': raw_pps,
            'Smoothed PPS': smoothed_pps,
            'Congestion Probability (%)': congestion_prob
        }])
        
        st.session_state.history = pd.concat([st.session_state.history, new_row], ignore_index=True).tail(20)

        # 6. Render Live Analytics Chart
        chart_data = st.session_state.history.set_index('Time')[['Smoothed PPS', 'Congestion Probability (%)']]
        chart_box.line_chart(chart_data)

else:
    status_box.info("👈 Select your Wi-Fi interface and check 'Start Live Network Sniffing' in the sidebar.")