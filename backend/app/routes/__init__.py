from flask import Blueprint, request, jsonify
import joblib
import numpy as np

main_bp = Blueprint('main', __name__)

@main_bp.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    kelembaban = data.get('kelembaban')
    suhu = data.get('suhu')
    cuaca = data.get('cuaca')

    try:
        # Load encoder dan model
        encoder = joblib.load('app/dbd/label_encoder.pkl')  # pastikan path benar
        cuaca_encoded = encoder.transform([cuaca])[0]
        
        input_data = np.array([[kelembaban, suhu, cuaca_encoded]])

        # Load semua model
        model_dbd = joblib.load('app/dbd/model_rfr.pkl')
        model_ispa = joblib.load('app/ispa/model_rfr.pkl')
        model_influenza = joblib.load('app/influenza/model_rfr.pkl')

        # Prediksi
        pred_dbd = model_dbd.predict(input_data)[0]
        pred_ispa = model_ispa.predict(input_data)[0]
        pred_influenza = model_influenza.predict(input_data)[0]

        return jsonify({
            'status': 'success',
            'predictions': {
                'dbd': int(pred_dbd),
                'ispa': int(pred_ispa),
                'influenza': int(pred_influenza)
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
