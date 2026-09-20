import streamlit as st
import pandas as pd
import joblib

# Set page configuration
st.set_page_config(
    page_title="Network Congestion Predictor",
    page_icon="🌐",
    layout="centered"
)

# Load the trained model
@st.cache_resource
def load_model():
    return joblib.load("congestion_model.pkl")

model = load_model()

st.title("🌐 Network Traffic Congestion Predictor")
st.write("Adjust network telemetry parameters below to test the Machine Learning model in real time.")

st.divider()

# Input controls using sliders and numeric inputs
st.subheader("📊 Network Metrics Input")

col1, col2 = st.columns(2)

with col1:
    packets_per_sec = st.number_input("Packets per Second (PPS)", min_value=0.0, max_value=100000.0, value=1200.0, step=50.0)
    packet_size = st.number_input("Average Packet Size (Bytes)", min_value=0.0, max_value=1500.0, value=500.0, step=10.0)

with col2:
    bytes_transferred = st.number_input("Total Traffic Volume (Bytes)", min_value=0.0, max_value=10000000.0, value=600000.0, step=10000.0)
    duration = st.number_input("Flow Duration (Seconds)", min_value=0.0, max_value=3600.0, value=10.0, step=1.0)

st.divider()

# Prepare feature vector for prediction matching model's expected column names
input_data = pd.DataFrame([{
    'Packets_Per_Second': packets_per_sec,
    'Packet_Size': packet_size,
    'Traffic_Volume_Bytes': bytes_transferred,
    'Flow_Duration': duration
}])

# Make prediction
if st.button("🚀 Analyze Traffic Flow", use_container_width=True):
    # Align dataframe with model's expected feature names if available
    if hasattr(model, 'feature_names_in_'):
        input_data = input_data.reindex(columns=model.feature_names_in_)

    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]
    
    congestion_prob = probabilities[1] * 100
    normal_prob = probabilities[0] * 100

    st.subheader("🎯 Prediction Result")
    
    if prediction == 1:
        st.error(f"🚨 **CONGESTED NETWORK DETECTED** ({congestion_prob:.1f}% Confidence)")
        st.write("Network bandwidth threshold exceeded (> 0.70 utilization). Potential traffic bottleneck or packet drop expected.")
    else:
        st.success(f"✅ **NORMAL NETWORK OPERATION** ({normal_prob:.1f}% Confidence)")
        st.write("Traffic flow is within healthy operational parameters.")

    # Show confidence metrics
    st.progress(int(congestion_prob) / 100)
    st.caption(f"Congestion Probability Metric: {congestion_prob:.2f}%")