from flask import Blueprint, request, jsonify

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        kelembaban = data['kelembaban']
        suhu = data['suhu']
        cuaca = data['cuaca']

        # Contoh dummy prediksi (ganti dengan model asli)
        return jsonify({
            'status': 'success',
            'predictions': {
                'dbd': 12,
                'ispa': 23,
                'influenza': 5
            }
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
