from flask import Flask, jsonify
from sqlalchemy import text
from dotenv import load_dotenv
from extensions import db
from models.user import User
import os

load_dotenv()

app = Flask(__name__)

# MySQL configuration
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "TutorHomes Flask Server is Running!"


@app.route("/api/health")
def health():
    try:
        db.session.execute(text("SELECT 1"))

        return jsonify({
            "status": "success",
            "backend": "connected",
            "database": "connected",
            "message": "TutorHomes Backend and MySQL are Connected"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "backend": "connected",
            "database": "disconnected",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)