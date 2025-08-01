#!/bin/bash -Valencia Walker's run.sh
export FLASK_APP=app.py
export FLASK_ENV=development
export CESIUM_ION_ACCESS_TOKEN="your_cesium_ion_access_token_here"
flask run --host=0.0.0.0 --port=5000
