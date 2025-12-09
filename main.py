from flask import Flask, request, jsonify
from dotenv import load_dotenv
import stripe
import os
import logging

load_dotenv()

logging.basicConfig(
    filename=os.getenv('LOG_FILE'),
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)


@app.route('/')
def index():
    return '{"msg":"gods_shadow_payment v1.0"}'


@app.route('/create_link', methods=['POST'])
def create_link():
    data = request.get_json()

    stripe.api_key = os.getenv('STRIPE_API_KEY')

    currency = "USD"
    unit_amount = data.get('unit_amount')
    # qty = data.get('qty')
    product_name = data.get('product_name')
    desc = data.get('desc')

    if unit_amount <= 0:
        logging.error('unit_amount must be greater than 0.')
        return jsonify({"error": "unit_amount must be greater than 0."}, 400)

    # if qty <= 0:
    #     logging.error('you must have at least 1 item.')
    #     return jsonify({"error": "you must have at least 1 item."}, 400)

    if len(product_name.strip()) == 0:
        logging.error('a product name is required.')
        return jsonify({"error": "a product name is required."}, 400)

    if len(desc.strip()) == 0:
        desc = "N/A"

    price_data_ = {
        "quantity": 1,
        "price_data": {
            "currency": currency,
            "product_data": {
                "name": product_name,
                "description": desc,
            },
            "unit_amount": round(unit_amount)
        },
    }

    payment_method_types_ = ["card", "us_bank_account"]

    try:
        res = stripe.PaymentLink.create(
            payment_method_types=payment_method_types_,
            line_items=[price_data_],
        )

        logging.info("payment link generated successfully: " + res['url'])
        return jsonify({"success": res}, 200)

    except Exception as e:
        logging.error(str(e))
        return jsonify({"error": "an error occurred"}, 200)


if __name__ == '__main__':
    app.run(debug=True)
