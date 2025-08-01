# physics_sim.py-Valencia Walker's

import math
import time
import random

# -------------------------------
# Motor Simulation State
# -------------------------------

motor_state = {
    "motor_id": "M1",
    "rpm": 0,
    "target_rpm": 3200,
    "torque_nm": 0.0,
    "direction": "clockwise",
    "status": "idle",
    "angular_velocity": 0.0,  # rad/s
    "temperature_c": 25.0,
    "failures": [],
}

# -------------------------------
# Robot Arm Simulation State
# -------------------------------

arm_state = {
    "arm_id": "A1",
    "current_position_deg": 0,
    "target_position_deg": 0,
    "movement": "idle",
    "speed_dps": 45,
    "temperature_c": 24.0,
    "servo_load": 0.0,
    "failures": []
}

# -------------------------------
# Motor Simulation Logic
# -------------------------------

def spin_motor_simulation():
    step_rpm = 400
    cooling_rate = 0.5
    heat_rate = 0.75
    max_temp = 90

    if "overheat" in motor_state["failures"]:
        motor_state["status"] = "failed"
        return motor_state

    # Spin up logic
    if motor_state["rpm"] < motor_state["target_rpm"]:
        motor_state["rpm"] += step_rpm
        motor_state["status"] = "spinning up"
    elif motor_state["rpm"] > motor_state["target_rpm"]:
        motor_state["rpm"] -= step_rpm
        motor_state["status"] = "slowing"
    else:
        motor_state["status"] = "steady"

    # Clamp RPM
    motor_state["rpm"] = min(motor_state["rpm"], motor_state["target_rpm"])

    # Torque = arbitrary function of RPM
    motor_state["torque_nm"] = round(math.log(motor_state["rpm"] + 1) * 0.08, 3)

    # Angular velocity (rad/s)
    motor_state["angular_velocity"] = round((motor_state["rpm"] * 2 * math.pi) / 60, 2)

    # Heat simulation
    motor_state["temperature_c"] += heat_rate
    if motor_state["status"] == "idle":
        motor_state["temperature_c"] -= cooling_rate
    motor_state["temperature_c"] = round(motor_state["temperature_c"], 2)

    # Simulate overheat
    if motor_state["temperature_c"] >= max_temp:
        motor_state["failures"].append("overheat")
        motor_state["status"] = "failed"

    return dict(motor_state)


# -------------------------------
# Robot Arm Simulation Logic
# -------------------------------

def move_robot_arm(target_deg: int):
    max_deg = 180
    min_deg = 0
    target = max(min(target_deg, max_deg), min_deg)
    delta = target - arm_state["current_position_deg"]

    arm_state["target_position_deg"] = target

    if abs(delta) < 1:
        arm_state["movement"] = "reached"
        arm_state["servo_load"] = 0.0
    else:
        # Move toward target
        direction = 1 if delta > 0 else -1
        step = direction * arm_state["speed_dps"] * 0.1  # simulate 100ms/frame
        arm_state["current_position_deg"] += step
        arm_state["current_position_deg"] = round(arm_state["current_position_deg"], 2)
        arm_state["movement"] = "moving"
        arm_state["servo_load"] = round(abs(delta) / 180, 2)

    # Simulate servo heating
    if arm_state["movement"] == "moving":
        arm_state["temperature_c"] += 0.4
    else:
        arm_state["temperature_c"] -= 0.3

    # Clamp temperature
    arm_state["temperature_c"] = round(max(24.0, min(80.0, arm_state["temperature_c"])), 2)

    # Simulate failure
    if arm_state["temperature_c"] > 75 and "servo_fail" not in arm_state["failures"]:
        arm_state["failures"].append("servo_fail")
        arm_state["movement"] = "failed"

    return dict(arm_state)
