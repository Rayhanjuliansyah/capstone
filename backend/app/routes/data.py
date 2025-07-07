from flask import Blueprint, jsonify

data_bp = Blueprint('data', __name__)

@data_bp.route('/data', methods=['GET'])
def get_data():
    # Contoh dummy, bisa diganti dengan membaca dari file/dataset/model
    return jsonify([
        {"tanggal": "2025-07-01", "dbd": 10, "ispa": 5, "influenza": 3},
        {"tanggal": "2025-07-02", "dbd": 12, "ispa": 6, "influenza": 4}
    ])
