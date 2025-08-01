#utils.py-Valencia Walker's

import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

def get_env_variable(name: str, default=None):
    """Safely get an environment variable or return a default value."""
    value = os.getenv(name, default)
    if value is None:
        log_error(f"Environment variable '{name}' is not set.")
    return value

def log_info(message: str):
    logging.info(message)

def log_error(message: str):
    logging.error(message)

def current_timestamp() -> str:
    """Return the current UTC timestamp in ISO 8601 format."""
    return datetime.utcnow().isoformat() + "Z"

def read_json(file_path: str) -> dict:
    """Read and return JSON data from a file."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        log_error(f"JSON file not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        log_error(f"Error decoding JSON from file: {file_path}")
        return {}

def get_cesium_token():
    """Retrieve the Cesium access token from environment variables."""
    return get_env_variable("CESIUM_ACCESS_TOKEN", "DEFAULT_CESIUM_TOKEN")
