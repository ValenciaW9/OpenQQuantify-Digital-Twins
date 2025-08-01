// static/js/cesium_controller.js-Valencia Walker's

async function uploadToCesium(file) {
  const formData = new FormData();
  formData.append("model", file);
  const res = await fetch("/api/upload_model", {
    method: "POST",
    body: formData
  });
  const result = await res.json();
  if (result.asset_id) alert("Upload Successful. Asset ID: " + result.asset_id);
  else alert("Upload failed: " + result.error);
}

function startMotorSimulation() {
  const socket = io();
  socket.on("motor_update", data => {
    document.getElementById("motor-status").innerText = `Motor RPM: ${data.rpm}`;
  });
  fetch("/api/simulate_motor");
}

function moveRobotArm() {
  const socket = io();
  socket.on("arm_position", data => {
    document.getElementById("arm-status").innerText = `Arm Position: ${data.degrees.join(", ")}`;
  });
  fetch("/api/move_arm");
}
