from flask import Flask, request, jsonify
from dotenv import load_dotenv
import stripe
import os
import logging
import core

load_dotenv()

# logging.basicConfig(
#     filename=os.getenv('LOG_FILE'),
#     filemode='a',
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"status": 200,
                    "message": "gods_shadow_v1.0",
                    })


@app.route('/currencies')
def get_supported_currencies():
    return jsonify({"status": 200,
                    "message": "fetched currencies successfully",
                    "data": core.get_currencies()
                    })


@app.route('/create_link', methods=['POST'])
def create_invoice_link():
    stripe.api_key = os.getenv('STRIPE_API_KEY')
    data = request.get_json()

    # get request data
    amount = data.get('amount')
    customer_name = data.get('customer_name')
    customer_email = data.get('customer_email')
    desc = data.get('desc')
    currency = data.get('currency')
    days_until_due = data.get('days_until_due')

    # validation
    if amount <= 0:
        logging.error('amount must be greater than 0.')
        return jsonify({"status": 400,
                        "message": "amount must be greater than 0.",
                        "data": []
                        })

    if len(customer_name.strip()) == 0:
        logging.error("the client's name is required")
        return jsonify({"status": 400,
                        "message": "the client's name is required",
                        "data": []
                        })

    if len(customer_email.strip()) == 0:
        logging.error("the client's email is required")
        return jsonify({"status": 400,
                        "message": "the client's email is required",
                        "data": []
                        })

    if len(desc.strip()) == 0:
        logging.error('the invoice description is required')
        return jsonify({"status": 400,
                        "message": "the invoice description is required",
                        "data": []
                        })

    if len(currency.strip()) == 0:
        logging.error('the transaction currency is required')
        return jsonify({"status": 400,
                        "message": "the transaction currency is required",
                        "data": []
                        })

    if days_until_due <= 0:
        logging.error('days_until_due must be greater than 0')
        return jsonify({"status": 400,
                        "message": "days_until_due must be greater than 0",
                        "data": []
                        })

    # validate currency selection
    currencies = core.get_currencies()
    currency_lookup = {cur["iso"]: cur["name"] for cur in currencies}

    if currency not in currency_lookup:
        logging.error('the transaction currency is invalid')
        return jsonify({"status": 400,
                        "message": "the transaction currency is invalid",
                        "data": []
                        })

    #
    # price_data_ = {
    #     "quantity": 1,
    #     "price_data": {
    #         "currency": currency,
    #         "product_data": {
    #             "name": product_name,
    #             "description": desc,
    #         },
    #         "unit_amount": unit_amount * 100
    #     },
    # }

    # Create customer

    try:
        customer = core.create_customer(name=customer_name, email=customer_email)
        payment_settings = core.get_payment_settings(currency_iso=currency)
        invoice = core.create_invoice(customer_id=customer.id,
                                      currency_iso=currency,
                                      payment_settings=payment_settings,
                                      days_until_due=days_until_due)
        invoice_item = core.create_invoice_item(customer.id,
                                                amount * 100,
                                                currency,
                                                desc,
                                                invoice.id)

        invoice_url = core.get_hosted_invoice_link(invoice_item)

        return jsonify({"status": 200,
                        "message": "url generated successfully",
                        "data": [
                            {"invoice_url": invoice_url}
                        ]
                        })

    except Exception as e:
        logging.error(str(e))
        print(str(e))
        return jsonify({"error": "an error occurred"}, 200)


if __name__ == '__main__':
    app.run(debug=True)
