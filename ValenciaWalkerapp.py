#ValenciaWalker for Digital Twins still working on app.py and other phases within the project.
# ValenciaWalker – Finalized app.py for OpenQQuantify Digital Twins

from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from flask_socketio import SocketIO
from backend.agents import run_ai_agent
from backend.iot_simulator import simulate_temperature
from backend.bom_marketplace import generate_bom, create_checkout_session
from backend.cesium_manager import upload_model_to_cesium
from backend.physics_sim import spin_motor_simulation, move_robot_arm
from backend.code_executor import execute_user_code
from backend.templates_api import save_template, load_template
from backend.utils import get_cesium_token
import threading
import time
import os
import eventlet


# Monkey patch for socket IO
eventlet.monkey_patch()


# Load .env variables
load_dotenv()

# Init Flask + SocketIO
app = Flask(__name__, static_folder="static", template_folder="templates")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "openq_secret")
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

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

# ------------------------ Cesium Token ------------------------ #

@app.route("/api/cesium_token", methods=["GET"])
def get_cesium_token_api():
    return jsonify({"token": get_cesium_token()})

# ------------------------ Static Files ------------------------ #

pytho@app.route("/static/<path:path>")
def static_files(path):
    return send_from_directory("static", path)

# ------------------------ Real-Time Socket Stream ------------------------ #

def emit_simulation_data():
    while True:
        motor = spin_motor_simulation()
        arm = move_robot_arm(135)
        socketio.emit('sim_update', {"motor": motor, "arm": arm})
        time.sleep(1)

# Start real-time thread
threading.Thread(target=emit_simulation_data, daemon=True).start()

# ------------------------ Run App with SocketIO ------------------------ #

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port, debug=True)
