import joblib
import pandas as pd

# 1. Load the trained model
model = joblib.load('congestion_model.pkl')

# 2. List the features
features = ['Traffic Volume (Bytes)', 'Packets per Second (PPS)', 'Packet Size', 'Flow Duration']

# 3. Create a clean display of feature importances
importance_df = pd.DataFrame({
    'Metric': features,
    'Importance Score': model.feature_importances_
}).sort_values(by='Importance Score', ascending=False)

print("\n--- Network Congestion Feature Importance ---")
print(importance_df.to_string(index=False))