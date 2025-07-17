from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
import numpy as np
import joblib
import os

router = APIRouter()

# ===== Mapping cuaca ke angka (sesuai pelatihan model) =====
cuaca_mapping = {
    "Cerah": 0,
    "Berawan": 1,
    "Hujan Ringan": 2,
    "Hujan Sedang": 3,
    "Hujan Lokal": 4,
    "Hujan Petir": 5
}

# ===== Schema input =====
class InputData(BaseModel):
    kelembaban: float
    suhu: float
    cuaca: str
    tanggal: str

# ===== Load model (pakai path relatif dari file ini) =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # = /backend/app/routes

# naik 2 folder ke /backend
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

model_dbd = joblib.load(os.path.join(ROOT_DIR, "app", "dbd", "model_rfr.pkl"))
model_ispa = joblib.load(os.path.join(ROOT_DIR, "app", "ispa", "model_rfr.pkl"))
model_influenza = joblib.load(os.path.join(ROOT_DIR, "app", "influenza", "model_rfr.pkl"))


# ===== Endpoint prediksi =====
@router.post("/predict")
def predict(data: InputData) -> Dict:
    try:
        if data.cuaca not in cuaca_mapping:
            raise HTTPException(status_code=400, detail=f"Cuaca '{data.cuaca}' tidak valid.")

        cuaca_encoded = cuaca_mapping[data.cuaca]
        fitur = np.array([[data.suhu, data.kelembaban, cuaca_encoded]])

        pred_dbd = model_dbd.predict(fitur)[0]
        pred_ispa = model_ispa.predict(fitur)[0]
        pred_influenza = model_influenza.predict(fitur)[0]

        return {
            "status": "success",
            "tanggal": data.tanggal,
            "predictions": {
                "dbd": int(pred_dbd),
                "ispa": int(pred_ispa),
                "influenza": int(pred_influenza)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memproses prediksi: {str(e)}")
