import joblib
import pandas as pd

# Load your trained model
model = joblib.load('congestion_model.pkl')

print("=============================================")
print("  NETWORK TRAFFIC CONGESTION PREDICTOR  ")
print("=============================================")
print("Enter values between 0.0 and 1.0 (Press Ctrl+C to exit)\n")

while True:
    try:
        # Prompt user for inputs directly in the terminal
        tv = float(input("Enter Traffic Volume (0.0 - 1.0): "))
        pps = float(input("Enter Packets per Second (0.0 - 1.0): "))
        ps = float(input("Enter Packet Size (0.0 - 1.0): "))
        fd = float(input("Enter Flow Duration (0.0 - 1.0): "))

        # Format input into a DataFrame
        sample = pd.DataFrame([{
            'Traffic Volume (Bytes)': tv,
            'Packets per Second (PPS)': pps,
            'Packet Size': ps,
            'Flow Duration': fd
        }])

        # Predict
        pred = model.predict(sample)[0]
        prob = model.predict_proba(sample)[0][1]

        status = "🚨 CONGESTED" if pred == 1 else "✅ NORMAL"
        print(f"\n---> Result: {status} (Congestion Probability: {prob * 100:.1f}%)\n")
        print("-" * 45)

    except KeyboardInterrupt:
        print("\nExiting predictor. Goodbye!")
        break
    except ValueError:
        print("\nInvalid input! Please enter numbers only (e.g., 0.5, 0.85).\n")