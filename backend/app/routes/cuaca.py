import os
import httpx
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv

# Ambil path file .env yang berada dua folder di atas (../.. dari file ini)
dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path)  # Pastikan .env dibaca dari lokasi ini

router = APIRouter(prefix="/cuaca", tags=["Cuaca"])

@router.get("/today")
async def get_cuaca_today(kota: str = "Padang"):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    # DEBUG: Cek apakah API key berhasil terbaca
    if not api_key:
        print(">> API Key tidak ditemukan!")
        raise HTTPException(status_code=500, detail="API Key tidak ditemukan")

    print(">> API Key ditemukan:", api_key)  # Hapus ini setelah berhasil

    # URL untuk OpenWeatherMap API
    url = f"https://api.openweathermap.org/data/2.5/weather?q={kota}&appid={api_key}&units=metric"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data cuaca")

        data = response.json()

        return {
            "kota": kota,
            "suhu_sekarang": round(data["main"]["temp"]),
            "kelembapan": data["main"]["humidity"],
            "cuaca": data["weather"][0]["description"].capitalize()
        }
    
    except KeyError:
        raise HTTPException(status_code=500, detail="Format data dari API cuaca tidak sesuai")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {str(e)}")
