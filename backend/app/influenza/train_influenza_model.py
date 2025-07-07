import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# === Load data dari file CSV ===
data_path = "app/influenza/data_influenza.csv"
if not os.path.exists(data_path):
    raise FileNotFoundError("❌ File data_influenza.csv tidak ditemukan.")

df = pd.read_csv(data_path)

# === Encode cuaca ===
encoder = LabelEncoder()
df["cuaca_encoded"] = encoder.fit_transform(df["cuaca"])

# === Feature dan target ===
X = df[["kelembaban", "suhu", "cuaca_encoded"]]
y = df["jumlah_kasus"]

# === Train model ===
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# === Simpan model dan encoder ===
joblib.dump(model, "app/influenza/model_rfr.pkl")
joblib.dump(encoder, "app/influenza/label_encoder.pkl")

print("✅ Model Influenza berhasil dilatih dan disimpan.")
