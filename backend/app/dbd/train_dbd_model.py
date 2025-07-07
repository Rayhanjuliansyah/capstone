import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import os

# Load dataset
df = pd.read_csv("dataset_dbd.csv")  # Pastikan file berada di direktori yang sama

# Preprocessing
X = df[["kelembaban", "suhu", "cuaca"]].copy()
y = df["jumlah_kasus_dbd"]

# Encode fitur cuaca
encoder = LabelEncoder()
X["cuaca_encoded"] = encoder.fit_transform(X["cuaca"])
X = X[["kelembaban", "suhu", "cuaca_encoded"]]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluasi model
y_pred = model.predict(X_test)
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
print("R2 Score:", r2_score(y_test, y_pred))

# Simpan model dan encoder
os.makedirs("app/dbd", exist_ok=True)
joblib.dump(model, "app/dbd/model_rfr.pkl")
joblib.dump(encoder, "app/dbd/label_encoder.pkl")

print("✅ Model dan encoder berhasil disimpan.")
