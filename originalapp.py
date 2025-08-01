from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from agents import run_ai_agent
from iot_simulator import simulate_temperature
from bom_marketplace import generate_bom, create_checkout_session
from cesium_manager import upload_model_to_cesium
from physics_sim import spin_motor_simulation, move_robot_arm
from code_executor import execute_user_code
from templates_api import save_template, load_template
from utils import get_cesium_token
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Enable CORS for all routes

# ------------------------ Web Interface ------------------------ #

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# ------------------------ AI Agent ------------------------ #

@app.route("/api/agent", methods=["POST"])
def agent_prompt():
    body = request.get_json()
    prompt = body.get("prompt")
    task_type = body.get("task_type", "general")
    response = run_ai_agent(prompt, task_type)
    return jsonify({"result": response})

# ------------------------ Sensor Simulator ------------------------ #

@app.route("/api/iot", methods=["GET"])
def simulate():
    data = simulate_temperature()
    return jsonify(data)

# ------------------------ Cesium Upload ------------------------ #

@app.route("/api/upload_model", methods=["POST"])
def upload_model():
    body = request.get_json()
    success = upload_model_to_cesium(body.get("model_path"))
    return jsonify({"success": success})

# ------------------------ Motor & Robotics Sim ------------------------ #

@app.route("/api/simulate_motor", methods=["GET"])
def simulate_motor():
    return jsonify(spin_motor_simulation())

@app.route("/api/move_arm", methods=["POST"])
def simulate_arm():
    body = request.get_json()
    pos = body.get("position", 90)
    return jsonify(move_robot_arm(pos))

# ------------------------ Code IDE Execution ------------------------ #

@app.route("/api/execute", methods=["POST"])
def execute_code():
    body = request.get_json()
    code = body.get("code", "")
    output = execute_user_code(code)
    return jsonify({"output": output})

# ------------------------ BOM & Checkout ------------------------ #

@app.route("/api/bom", methods=["GET"])
def get_bom():
    bom = generate_bom()
    return jsonify(bom)

@app.route("/api/checkout", methods=["POST"])
def checkout():
    body = request.get_json()
    url = create_checkout_session(body["item"], body["price"])
    return jsonify({"url": url})

# ------------------------ Template Save/Load ------------------------ #

@app.route("/api/save_template", methods=["POST"])
def save_template_api():
    body = request.get_json()
    save_template(body["name"], body["data"])
    return jsonify({"status": "saved"})

@app.route("/api/load_template/<name>", methods=["GET"])
def load_template_api(name):
    data = load_template(name)
    return jsonify(data)

# ------------------------ Static Files ------------------------ #

@app.route("/static/<path:path>")
def static_files(path):
    return send_from_directory("static", path)

# ------------------------ Cesium ------------------------ #

@app.route("/api/cesium_token", methods=["GET"])
def get_cesium_token_api():
    return jsonify({"token": get_cesium_token()})

# ------------------------ Run App ------------------------ #

if __name__ == "__main__":
    # Optionally, get port from env, default 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)