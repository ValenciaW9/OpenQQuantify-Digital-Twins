## app.py -Valencia Walekr's
## app.py - Valencia Walker's

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os
import threading
import time
import eventlet

eventlet.monkey_patch()
load_dotenv()

from backend.cesium_manager import cesium_bp
from backend.agents import run_ai_agent
from backend.iot_simulator import simulate_temperature
from backend.bom_marketplace import generate_bom, create_checkout_session, bom_api
from backend.physics_sim import spin_motor_simulation, move_robot_arm
from backend.code_executor import execute_user_code
from backend.templates_api import save_template, load_template
from backend.utils import get_cesium_token
from backend.__init__ import register_routes
from database.database import create_db_and_tables


app = Flask(__name__, static_folder="static", template_folder="templates")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "openq_secret")
CORS(app)

# Register Blueprints
app.register_blueprint(cesium_bp)
app.register_blueprint(bom_api)

register_routes(app)
create_db_and_tables()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/ai-agent", methods=["POST"])
def ai_agent():
    data = request.json
    prompt = data.get("prompt", "")
    task_type = data.get("task_type", "general")
    result = run_ai_agent(prompt, task_type)
    return jsonify({"response": result})

@app.route("/api/bom", methods=["POST"])
def bom():
    data = request.json
    result = generate_bom(data)
    return jsonify(result)

@app.route("/api/checkout", methods=["POST"])
def checkout():
    data = request.json
    session = create_checkout_session(data)
    return jsonify(session)

def emit_simulation_data():
    while True:
        motor_data = spin_motor_simulation()
        arm_data = move_robot_arm(135)
        temp_data = simulate_temperature()

        # Example output: replace with socketio emit if real-time frontend integration
        print("Motor Simulation Data:", motor_data)
        print("Robot Arm Simulation Data:", arm_data)
        print("Temperature Sensor Data:", temp_data)

        time.sleep(1)

threading.Thread(target=emit_simulation_data, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
