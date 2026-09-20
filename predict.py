import joblib
import pandas as pd

# Load the saved model
print("Loading model...")
model = joblib.load('congestion_model.pkl')

def predict_congestion(traffic_volume, pps, packet_size, flow_duration):
    sample = pd.DataFrame([{
        'Traffic Volume (Bytes)': traffic_volume,
        'Packets per Second (PPS)': pps,
        'Packet Size': packet_size,
        'Flow Duration': flow_duration
    }])
    
    prediction = model.predict(sample)[0]
    probability = model.predict_proba(sample)[0][1]
    
    status = "CONGESTED 🚨" if prediction == 1 else "NORMAL ✅"
    print(f"Result: {status} (Congestion Probability: {probability * 100:.2f}%)")

print("\n--- Test 1: Low Network Activity ---")
predict_congestion(traffic_volume=0.05, pps=0.02, packet_size=0.10, flow_duration=0.01)

print("\n--- Test 2: High Network Spike ---")
predict_congestion(traffic_volume=0.85, pps=0.78, packet_size=0.65, flow_duration=0.90)