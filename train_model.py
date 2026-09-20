import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

print("1. Loading dataset...")
df = pd.read_csv('preprocessed_dataset.csv')

# Target variable (1 = Congested, 0 = Normal)
df['is_congested'] = (df['Bandwidth Utilization'] > 0.70).astype(int)

# Features (X) & Target (y)
X = df[['Traffic Volume (Bytes)', 'Packets per Second (PPS)', 'Packet Size', 'Flow Duration']]
y = df['is_congested']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest Model
print("\n2. Training Random Forest Model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Print accuracy
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"\nModel Accuracy: {accuracy * 100:.2f}%")

# SAVE THE MODEL TO DISK
joblib.dump(model, 'congestion_model.pkl')
print("\nSuccess: Saved model to 'congestion_model.pkl'!")