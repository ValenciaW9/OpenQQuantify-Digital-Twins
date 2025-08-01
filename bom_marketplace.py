# backend/bom_marketplace.py
import os
import stripe
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

bom_api = Blueprint('bom_api', __name__)

# Simulated inventory
INVENTORY = {
    "arduino_nano": 25.00,
    "raspberry_pi_4": 65.00,
    "nvidia_jetson_nano": 99.00,
    "esp32_devkit": 18.00,
    "temperature_sensor": 5.00,
    "motor_driver": 12.00,
    "servo_motor": 9.00,
    "led_array": 3.50,
    "lcd_display": 10.00,
    "voltage_regulator": 4.25
}

def calculate_markup_price(base_price, markup=0.10):
    return round(base_price * (1 + markup), 2)

@bom_api.route('/api/bom', methods=['POST'])
def generate_bom():
    """
    POST /api/bom
    Payload: { "components": ["component_1", "component_2", ...] }
    Returns: Bill of materials with pricing.
    """
    try:
        data = request.json
        components = data.get("components", [])

        if not components or not isinstance(components, list):
            return jsonify({"error": "Invalid or missing component list."}), 400

        bom_items = []
        total_cost = 0.0

        for part in components:
            if part not in INVENTORY:
                return jsonify({"error": f"Component '{part}' not found."}), 404

            base_price = INVENTORY[part]
            price_with_markup = calculate_markup_price(base_price)

            bom_items.append({
                "name": part,
                "base_price": base_price,
                "price_with_markup": price_with_markup
            })
            total_cost += price_with_markup

        return jsonify({
            "bill_of_materials": bom_items,
            "total": round(total_cost, 2)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bom_api.route('/api/checkout', methods=['POST'])
def create_checkout():
    """
    POST /api/checkout
    Payload: { "components": ["component_1", "component_2", ...] }
    Returns: Stripe checkout session URL
    """
    try:
        data = request.json
        components = data.get("components", [])

        if not components or not isinstance(components, list):
            return jsonify({"error": "Invalid or missing component list."}), 400

        line_items = []

        for part in components:
            if part not in INVENTORY:
                return jsonify({"error": f"Component '{part}' not found in inventory."}), 404

            price_cents = int(calculate_markup_price(INVENTORY[part]) * 100)

            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": part},
                    "unit_amount": price_cents
                },
                "quantity": 1
            })

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url="http://localhost:5000/success",
            cancel_url="http://localhost:5000/cancel"
        )

        return jsonify({"checkout_url": session.url}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
