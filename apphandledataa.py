from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time
import math
import uuid
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Simulation Parameters
MIN_DRONE_SPEED = 10.0      # meters per second
MAX_DRONE_SPEED = 20.0      # meters per second
PATH_UPDATE_INTERVAL = 30.0 # seconds between path updates
PATH_POINTS = 2              # number of waypoints to add each update
SPACING = 50.0               # horizontal spacing between drones
BASE_DISTANCE = 500.0        # distance ahead of camera to spawn drones
DRONE_HEIGHT_VARIATION = 50.0 # height variation in meters

# Manhattan Geographic Bounds
MANHATTAN_BOUNDS = {
    'west': -74.02,
    'east': -73.95,
    'south': 40.70,
    'north': 40.80
}

# Drone Storage
drones = {}
drones_lock = threading.Lock()

def lerp(start, end, t):
    return start + (end - start) * t

def random_lerp(start, end):
    return lerp(start, end, random.random())

def get_random_waypoint():
    lon = random_lerp(MANHATTAN_BOUNDS['west'], MANHATTAN_BOUNDS['east'])
    lat = random_lerp(MANHATTAN_BOUNDS['south'], MANHATTAN_BOUNDS['north'])
    height = random_lerp(100.0, 300.0)  # Height between 100m and 300m
    return {'lon': lon, 'lat': lat, 'height': height}

def get_circular_waypoints(center, radius, num_points, start_angle=0):
    waypoints = []
    for i in range(num_points):
        angle = start_angle + (2 * math.pi / num_points) * i
        lon = center['lon'] + (radius / 111320) * math.cos(angle)  # Approx meters to degrees
        lat = center['lat'] + (radius / 110540) * math.sin(angle)  # Approx meters to degrees
        height = random_lerp(100.0, 300.0)
        waypoints.append({'lon': lon, 'lat': lat, 'height': height})
    return waypoints

def get_linear_waypoints(point_a, point_b, num_points):
    waypoints = []
    for i in range(num_points):
        t = i / (num_points - 1)
        lon = lerp(point_a['lon'], point_b['lon'], t)
        lat = lerp(point_a['lat'], point_b['lat'], t)
        height = lerp(point_a['height'], point_b['height'], t)
        waypoints.append({'lon': lon, 'lat': lat, 'height': height})
    return waypoints

class Drone:
    def __init__(self, drone_id, initial_position, speed, trajectory_type):
        self.id = drone_id
        self.position = initial_position  # {'lon': float, 'lat': float, 'height': float}
        self.speed = speed
        self.trajectory_type = trajectory_type  # 'random', 'circular', 'linear'
        self.waypoints = []
        self.current_waypoint_index = 0
        self.last_update_time = time.time()
        self.assign_waypoints()

    def assign_waypoints(self):
        if self.trajectory_type == 'random':
            self.waypoints = [get_random_waypoint() for _ in range(PATH_POINTS)]
        elif self.trajectory_type == 'circular':
            center = get_random_waypoint()
            radius = random_lerp(500.0, 1500.0)  # Radius between 500m and 1500m
            self.waypoints = get_circular_waypoints(center, radius, PATH_POINTS)
        elif self.trajectory_type == 'linear':
            point_a = get_random_waypoint()
            point_b = get_random_waypoint()
            self.waypoints = get_linear_waypoints(point_a, point_b, PATH_POINTS)
        self.current_waypoint_index = 0

    def update_position(self, delta_time):
        if self.current_waypoint_index >= len(self.waypoints):
            self.assign_waypoints()

        target = self.waypoints[self.current_waypoint_index]
        distance = self.calculate_distance(self.position, target)
        max_distance = self.speed * delta_time

        if max_distance >= distance:
            # Move to the waypoint
            self.position = target
            self.current_waypoint_index += 1
        else:
            # Move proportionally towards the waypoint
            ratio = max_distance / distance
            self.position['lon'] = lerp(self.position['lon'], target['lon'], ratio)
            self.position['lat'] = lerp(self.position['lat'], target['lat'], ratio)
            self.position['height'] = lerp(self.position['height'], target['height'], ratio)

    def calculate_distance(self, pos1, pos2):
        # Simple Euclidean distance for small areas
        dx = (pos2['lon'] - pos1['lon']) * 111320 * math.cos(math.radians(pos1['lat']))  # meters
        dy = (pos2['lat'] - pos1['lat']) * 110540  # meters
        dz = pos2['height'] - pos1['height']  # meters
        return math.sqrt(dx*dx + dy*dy + dz*dz)

def simulation_loop():
    while True:
        with drones_lock:
            current_time = time.time()
            for drone in drones.values():
                delta_time = current_time - drone.last_update_time
                if delta_time >= PATH_UPDATE_INTERVAL:
                    drone.assign_waypoints()
                    drone.last_update_time = current_time
                drone.update_position(delta_time)
                drone.last_update_time = current_time
        time.sleep(1)  # Update every second

# Start the simulation loop in a background thread
simulation_thread = threading.Thread(target=simulation_loop, daemon=True)
simulation_thread.start()

@app.route('/api/spawn_drones', methods=['POST'])
def spawn_drones():
    data = request.get_json()
    count = data.get('count', 1)
    if not isinstance(count, int) or count < 1 or count > 1000:
        return jsonify({'error': 'Invalid count. Must be an integer between 1 and 1000.'}), 400

    spawned_drones = []
    with drones_lock:
        for _ in range(count):
            drone_id = str(uuid.uuid4())
            initial_position = get_random_waypoint()
            speed = random_lerp(MIN_DRONE_SPEED, MAX_DRONE_SPEED)
            trajectory_type = random.choice(['random', 'circular', 'linear'])
            drone = Drone(drone_id, initial_position, speed, trajectory_type)
            drones[drone_id] = drone
            spawned_drones.append({
                'id': drone_id,
                'position': drone.position,
                'speed': drone.speed,
                'trajectory_type': drone.trajectory_type
            })
    return jsonify({'spawned': spawned_drones}), 201

@app.route('/api/clear_drones', methods=['POST'])
def clear_drones():
    with drones_lock:
        drones.clear()
    return jsonify({'message': 'All drones have been cleared.'}), 200

@app.route('/api/get_drones', methods=['GET'])
def get_drones():
    with drones_lock:
        drones_data = []
        for drone in drones.values():
            drones_data.append({
                'id': drone.id,
                'position': drone.position,
                'speed': drone.speed,
                'trajectory_type': drone.trajectory_type
            })
    return jsonify({'drones': drones_data}), 200

if __name__ == '__main__':
    app.run(debug=True)