# OpenQQuantify Digital Twins Platform

## Overview
This is a full-stack simulation platform that enables real-time 3D Digital Twin modeling, AI-assisted electronics design, robotics & IoT simulation, and user-controlled code execution. Built for engineering teams and makers to develop and interact with smart machines in virtual space.



## Features
| Module                  | Description                                                         |
| ----------------------- | ------------------------------------------------------------------- |
| 🔧 2D→3D Export API     | Accepts schematic JSON and prepares OBJ export payload              |
|  BOM Marketplace      | Auto-generates Bill of Materials with Stripe Checkout               |
|  AI Code Assistant    | (Optional) Generates code using OpenAI agent                        |
|  Template Manager     | Save and load Digital Twin templates as JSON                        |
|  Cesium Model Upload | Upload `.glb` files to Cesium Ion API                               |
|  Membership Checkout  | Stripe-powered subscription (2000–20,000 tokens/month)              |
|  JWT Authentication   | Signup/Login flows with hashed password + JWT token                 |
|  Simulation Layout    | JSON-based Digital Twin model layouts (motors, arms, sensors, CPUs) |


#Project Structure

OpenQQuantify/
├── app.py                     # Main Flask app entry
├── run.sh                     # Start script
├── requirements.txt           # Dependencies
├── .env                       # API keys and secrets

├── backend/
│   ├── __init__.py            # Blueprint registration
│   ├── agents.py              # (Optional) OpenAI integration
│   ├── auth.py                # Signup/Login logic
│   ├── bom_marketplace.py     # BOM & Stripe API
│   ├── cesium_manager.py      # Upload to Cesium Ion
│   ├── cesium_routes.py       # Handles POST to upload
│   ├── export_routes.py       # 2D → 3D export stub
│   ├── templates_api.py       # Save/load templates
│   └── code_executor.py       # (Optional) Python code sandbox

├── static/
│   ├── css/style.css          # UI styles
│   ├── js/editor.js           # Monaco code editor
│   ├── js/cesium_controller.js# 3D interactions
│   └── assets/                # Static models (motor.glb, arm.glb)

├── templates/
│   ├── index.html             # Main frontend
│   ├── schematic.html         # Schematic builder
│   ├── login.html             # JWT login
│   ├── signup.html            # JWT signup
│   └── membership.html        # Stripe membership page

├── templates_data/
│   └── Sample Digital Twin.json  # Stored simulation templates

└── uploads/                   # Temporary Cesium model uploads

Sample JSON Templates

Template:Sample DigitalTwin.json

```
json
{
  "template_name": "Sample Digital Twin",
  "description": "A basic example template for a digital twin system.",
  "components": [
    {
      "type": "motor",
      "id": "motor_001",
      "parameters": {
        "rpm": 1500,
        "voltage": 12
      }
    },
    {
      "type": "robot_arm",
      "id": "arm_001",
      "parameters": {
        "length_cm": 50,
        "degrees_of_freedom": 6
      }
    }
  ]
}

3D Layout Payload (for /api/export/obj

```
json

{
  "components": [
    { "id": "motor_001", "type": "motor", "x": 0, "y": 0, "z": 0 },
    { "id": "sensor_001", "type": "sensor", "x": 2, "y": 0, "z": 0 },
    { "id": "controller", "type": "cpu", "x": 1, "y": 2, "z": 0 }
  ]
}

#Authentication
Signup
'''
http
POST /api/auth/signup
{
  "email": "user@example.com",
  "password": "mypassword"
}

Login
```http
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "mypassword"
}
Returns JWT token to be used in Authorization: Bearer header.

Stripe Checkout (Membership)
Choose from 3 plans:

$20/month — 2000 tokens

$50/month — 7000 tokens

$100/month — 20000 tokens

After payment, users email connect@openqquantify.com for early access.

esium Model Upload
Endpoint: POST /api/cesium/upload
FormData: file: my_model.glb
Uploads .glb models to Cesium Ion and returns an asset ID.

🔧 Setup & Installation
1. Clone + Setup

git clone https://github.com/yourusername/OpenQQuantify.git
cd OpenQQuantify
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Add .env
Create .env file:
OPENAI_API_KEY=your_openai_key
STRIPE_SECRET_KEY=your_stripe_key
STRIPE_PUBLISHABLE_KEY=your_publishable_key
CESIUM_ACCESS_TOKEN=your_cesium_token
JWT_SECRET=your_jwt_secret
DATABASE_URL=sqlite:///local.db

Run the App
bash run.sh
# or
python app.py


Key API Endpoints

| Route                      | Method | Description                 |
| -------------------------- | ------ | --------------------------- |
| `/api/auth/signup`         | POST   | User signup                 |
| `/api/auth/login`          | POST   | User login                  |
| `/api/bom`                 | POST   | Generate Bill of Materials  |
| `/api/checkout`            | POST   | Stripe checkout for BOM     |
| `/api/templates/save`      | POST   | Save digital twin template  |
| `/api/templates/load/<id>` | GET    | Load saved template         |
| `/api/export/obj`          | POST   | Export 3D model payload     |
| `/api/cesium/upload`       | POST   | Upload `.glb` to Cesium Ion |

#Contact
For support, partnerships, or early access:
connect@openqquantify.com