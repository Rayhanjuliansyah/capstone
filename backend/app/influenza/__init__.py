from flask import Blueprint, request, jsonify
from app.influenza import model, encoder, CUACA_DIIJINKAN

influenza_bp = Blueprint("influenza", __name__)

@influenza_bp.route("/influenza/predict", methods=["POST"])
def predict_influenza():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Data input tidak ditemukan."}), 400

        kelembaban = data.get("kelembaban")
        suhu = data.get("suhu")
        cuaca = data.get("cuaca")

        if kelembaban is None or suhu is None or cuaca is None:
            return jsonify({"error": "kelembaban, suhu, dan cuaca harus diisi."}), 400

        if cuaca not in CUACA_DIIJINKAN:
            return jsonify({
                "error": f"Cuaca '{cuaca}' tidak valid. Pilih salah satu dari: {CUACA_DIIJINKAN}"
            }), 400

        if cuaca not in encoder.classes_:
            return jsonify({
                "error": f"Cuaca '{cuaca}' tidak dikenali oleh model. Pastikan label encoder sesuai."
            }), 400

        cuaca_encoded = encoder.transform([cuaca])[0]
        X = [[kelembaban, suhu, cuaca_encoded]]
        prediksi = model.predict(X)[0]

        return jsonify({"prediksi_jumlah_kasus": round(prediksi, 2)})

    except Exception as e:
        return jsonify({"error": f"Terjadi kesalahan internal: {str(e)}"}), 500
