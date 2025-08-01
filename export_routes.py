# 2D-> 3D OBJ Export API stub export_routes.py -Valencia Walker's

# backend/export_routes.py – Full 2D to 3D OBJ export logic
from flask import Blueprint, jsonify, request, send_file
import os
import uuid

export_bp = Blueprint("export", __name__, url_prefix="/api/export")

# Directory to save generated OBJ files
EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

# Utility to generate a simple cube in OBJ format at x, y, z
def generate_cube_obj(x, y, z, size=1.0, id_offset=0):
    half = size / 2.0
    vertices = [
        (x - half, y - half, z - half),
        (x + half, y - half, z - half),
        (x + half, y + half, z - half),
        (x - half, y + half, z - half),
        (x - half, y - half, z + half),
        (x + half, y - half, z + half),
        (x + half, y + half, z + half),
        (x - half, y + half, z + half),
    ]
    faces = [
        (1, 2, 3, 4), (5, 6, 7, 8),
        (1, 5, 8, 4), (2, 6, 7, 3),
        (4, 3, 7, 8), (1, 2, 6, 5)
    ]
    obj = ""
    for v in vertices:
        obj += f"v {v[0]} {v[1]} {v[2]}\n"
    for f in faces:
        obj += f"f {f[0] + id_offset} {f[1] + id_offset} {f[2] + id_offset} {f[3] + id_offset}\n"
    return obj


@export_bp.route("/obj", methods=["POST"])
def export_obj():
    try:
        schematic_data = request.json
        components = schematic_data.get("components", [])

        if not components or not isinstance(components, list):
            return jsonify({"error": "Missing or invalid components list"}), 400

        obj_lines = []
        vertex_count = 0

        for comp in components:
            x = comp.get("x", 0)
            y = comp.get("y", 0)
            z = comp.get("z", 0)  # Optional; default to 0
            obj = generate_cube_obj(x, y, z, size=1.0, id_offset=vertex_count)
            obj_lines.append(obj)
            vertex_count += 8  # Each cube adds 8 vertices

        # Save to file
        filename = f"{uuid.uuid4().hex}.obj"
        path = os.path.join(EXPORT_DIR, filename)

        with open(path, "w") as f:
            f.write("".join(obj_lines))

        return send_file(path, mimetype='text/plain', as_attachment=True, download_name=filename)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
