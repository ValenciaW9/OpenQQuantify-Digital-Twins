import os
import json

TEMPLATES_PATH = "templates_data"

def save_template(name, data):
    filepath = os.path.join(TEMPLATES_PATH, f"{name}.json")
    with open(filepath, "w") as f:
        json.dump(data, f)

def load_template(name):
    filepath = os.path.join(TEMPLATES_PATH, f"{name}.json")
    if not os.path.isfile(filepath):
        return None
    with open(filepath, "r") as f:
        return json.load(f)
