# Valencia Walker's cesium_manager.py
# backend/cesium_manager.py – Valencia Walker's Updated

import os
import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

CESIUM_ACCESS_TOKEN = os.getenv("CESIUM_ACCESS_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {CESIUM_ACCESS_TOKEN}"
}

UPLOAD_URL = "https://api.cesium.com/v1/assets"

cesium_bp = Blueprint('cesium', __name__)

@cesium_bp.route("/api/upload_model", methods=["POST"])
def upload_model():
    file = request.files.get("model")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Upload to Cesium Ion
    files = {
        "file": (file.filename, file.stream, file.mimetype)
    }
    data = {
        "name": file.filename,
        "type": "3D Tiles"
    }

    response = requests.post(UPLOAD_URL, headers=HEADERS, data=data, files=files)

    if response.status_code == 201:
        asset_info = response.json()
        return jsonify({
            "message": "Upload successful",
            "asset_id": asset_info["id"]
        })
    else:
        return jsonify({
            "error": "Cesium upload failed",
            "details": response.text
        }), 500
