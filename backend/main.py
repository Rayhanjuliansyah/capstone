from flask import Flask
from flask_cors import CORS  # ← tambahkan ini
from app.routes.predict import predict_bp
from app.routes.data import data_bp  # kalau ada

app = Flask(__name__)
CORS(app)  # ← aktifkan CORS di seluruh app

# Register route
app.register_blueprint(predict_bp, url_prefix="/api")
app.register_blueprint(data_bp, url_prefix="/api")  # kalau kamu juga pakai /api/data

if __name__ == "__main__":
    app.run(debug=True)
