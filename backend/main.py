from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import os
from datetime import datetime

from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

# Import router cuaca dan cuaca riwayat
from app.routes import cuaca
# from app.routes import cuaca_riwayat  

# Inisialisasi FastAPI
app = FastAPI()

# CORS untuk izinkan frontend mengakses
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)


app.include_router(cuaca.router)
# app.include_router(cuaca_riwayat.router)  

# Dependency untuk koneksi DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Load model ML
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
model_dbd = joblib.load(os.path.join(BASE_PATH, "app", "dbd", "model_rfr.pkl"))
model_ispa = joblib.load(os.path.join(BASE_PATH, "app", "ispa", "model_rfr.pkl"))
model_influenza = joblib.load(os.path.join(BASE_PATH, "app", "influenza", "model_rfr.pkl"))

# Mapping nilai cuaca ke angka
cuaca_mapping = {
    "Cerah": 0,
    "Berawan": 1,
    "Hujan Ringan": 2,
    "Hujan Sedang": 3,
    "Hujan Lokal": 4,
    "Hujan Petir": 5
}

# Skema input untuk prediksi
class InputData(BaseModel):
    suhu: float
    kelembapan: float
    cuaca: str
    tanggal: str  

# Endpoint prediksi dan simpan ke DB
@app.post("/predict")
def predict_all(data: InputData, db: Session = Depends(get_db)):
    if data.cuaca not in cuaca_mapping:
        raise HTTPException(status_code=400, detail="Cuaca tidak valid.")

    try:
        tanggal_obj = datetime.strptime(data.tanggal, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Format tanggal harus YYYY-MM-DD")

    fitur = np.array([[data.suhu, data.kelembapan, cuaca_mapping[data.cuaca]]])

    pred_dbd = model_dbd.predict(fitur)[0]
    pred_ispa = model_ispa.predict(fitur)[0]
    pred_influenza = model_influenza.predict(fitur)[0]

    
    hasil = models.Prediction(
        tanggal=tanggal_obj,
        dbd=int(pred_dbd),
        ispa=int(pred_ispa),
        influenza=int(pred_influenza)
    )
    db.add(hasil)
    db.commit()

    return {
        "status": "success",
        "tanggal": data.tanggal,
        "predictions": {
            "dbd": int(pred_dbd),
            "ispa": int(pred_ispa),
            "influenza": int(pred_influenza)
        }
    }

# Endpoint untuk ambil semua data riwayat prediksi
@app.get("/riwayat")
def get_all_predictions(db: Session = Depends(get_db)):
    data = db.query(models.Prediction).order_by(models.Prediction.tanggal.desc()).all()
    return {
        "status": "success",
        "data": [
            {
                "tanggal": str(row.tanggal),
                "dbd": row.dbd,
                "ispa": row.ispa,
                "influenza": row.influenza
            } for row in data
        ]
    }
    
#endpoint untuk visualisasi
@app.get("/riwayat/filter")
def get_predictions_by_date(
    start: str = Query(..., description="Tanggal awal dalam format YYYY-MM-DD"),
    end: str = Query(..., description="Tanggal akhir dalam format YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")

        data = db.query(models.Prediction)\
            .filter(models.Prediction.tanggal >= start_date)\
            .filter(models.Prediction.tanggal <= end_date)\
            .order_by(models.Prediction.tanggal)\
            .all()

        return {
            "status": "success",
            "data": [
                {
                    "tanggal": str(row.tanggal),
                    "dbd": row.dbd,
                    "ispa": row.ispa,
                    "influenza": row.influenza
                } for row in data
            ]
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Gagal memproses tanggal: {str(e)}"
        }

# Endpoint root
@app.get("/")
def root():
    return {"message": "API aktif"}
