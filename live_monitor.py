import time
import joblib
import pandas as pd
from scapy.all import sniff, IP

# Load model and dynamically retrieve the exact feature order used during fit
model = joblib.load("congestion_model.pkl")
expected_features = model.feature_names_in_

print(f"✅ Model successfully loaded. Expecting features in this exact order:")
print(expected_features)

packet_count = 0
total_bytes = 0
start_time = time.time()

def process_packet(packet):
    global packet_count, total_bytes, start_time
    
    if packet.haslayer(IP):
        packet_count += 1
        total_bytes += len(packet)
        
        elapsed_time = time.time() - start_time
        
        if elapsed_time >= 2.0:
            pps = packet_count / elapsed_time
            avg_size = total_bytes / packet_count if packet_count > 0 else 0
            
            # Map calculated values to the exact feature names required
            data = {
                'Flow Duration': elapsed_time,
                'Packet Size': avg_size,
                'Packets per Second (PPS)': pps,
                'Traffic Volume (Bytes)': total_bytes
            }
            
            # Build DataFrame matching the exact order expected by the model
            features = pd.DataFrame([data])[expected_features]
            
            prediction = model.predict(features)[0]
            status = "🚨 CONGESTED" if prediction == 1 else "✅ NORMAL"
            
            print(f"[{status}] PPS: {pps:.1f} | Avg Size: {avg_size:.1f} B | Rate: {(total_bytes * 8) / (elapsed_time * 1024):.1f} Kbps")
            
            # Reset counters
            packet_count = 0
            total_bytes = 0
            start_time = time.time()

print("\n🌐 Starting Live Network Sniffer (Press Ctrl+C to stop)...")
sniff(prn=process_packet, store=False)ru  