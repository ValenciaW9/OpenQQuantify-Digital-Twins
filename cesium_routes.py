# Valencia Walker's Cesium_routes.py

from flask import Blueprint, request, jsonify
from backend.cesium_manager import upload_asset_to_cesium
import os

cesium_bp = Blueprint("cesium", __name__, url_prefix="/api/cesium")

@cesium_bp.route("/upload", methods=["POST"])
def upload_model():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = file.filename
    save_path = os.path.join("uploads", filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(save_path)

    try:
        asset_id = upload_asset_to_cesium(save_path, filename)
        return jsonify({"asset_id": asset_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
