import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import os

data = {
    "kelembaban": [80, 70, 85, 90, 75, 60],
    "suhu": [28, 30, 27, 26, 29, 31],
    "cuaca": ["Cerah", "Hujan Ringan", "Berawan", "Hujan Petir", "Cerah", "Hujan Lokal"],
    "jumlah_kasus": [100, 200, 150, 300, 120, 220]
}

df = pd.DataFrame(data)

# === Encode kolom cuaca ===
encoder = LabelEncoder()
df["cuaca_encoded"] = encoder.fit_transform(df["cuaca"])

# === Feature dan target ===
X = df[["kelembaban", "suhu", "cuaca_encoded"]]
y = df["jumlah_kasus"]

# === Training model ===
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# === Simpan model dan encoder ===
os.makedirs("app/ispa", exist_ok=True)
joblib.dump(model, "app/ispa/model_rfr.pkl")
joblib.dump(encoder, "app/ispa/label_encoder.pkl")

print("✅ Model ISPA dan Label Encoder berhasil disimpan.")
