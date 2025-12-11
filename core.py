import stripe
from dotenv import load_dotenv
import os

load_dotenv()


def create_customer(name, email):
    customer = stripe.Customer.create(
        name=name,
        email=email
    )

    return customer


def get_currencies():
    currencies = [
        {"iso": "usd", "name": "US Dollar"},
        {"iso": "gbp", "name": "British Pound"},
        {"iso": "cad", "name": "Canadian Dollar"},
        {"iso": "eur", "name": "Euro"}
    ]

    return currencies


def get_payment_settings(currency_iso):
    payment_settings = ''

    if currency_iso == "usd":
        payment_settings = {
            "payment_method_types": [
                "card",
                "ach_debit",
                "us_bank_account",
                "link",
                "crypto"
            ],
        }

    elif currency_iso == "gbp":
        payment_settings = {
            "payment_method_types": [
                "card",
                "bacs_debit",
                "link"
            ],
        }

    elif currency_iso == "cad":
        payment_settings = {
            "payment_method_types": [
                "card",
                "acss_debit",
                "link",
            ],
        }

    elif currency_iso == "eur":
        payment_settings = {
            "payment_method_types": [
                "card",
                "sepa_debit",
                "link",
            ],
        }

    return payment_settings


def create_invoice(customer_id, currency_iso, payment_settings, days_until_due):
    invoice = stripe.Invoice.create(
        customer=customer_id,
        collection_method="send_invoice",
        days_until_due=days_until_due,
        payment_settings=payment_settings,
        currency=currency_iso
    )

    return invoice


def create_invoice_item(customer_id, amount, currency_iso, desc, invoice_id):
    stripe.InvoiceItem.create(
        customer=customer_id,
        amount=amount,  # Amount in cents !!VERY IMPORTANT!!
        currency=currency_iso,
        description=desc,
        invoice=invoice_id
    )

    finalized = stripe.Invoice.finalize_invoice(invoice_id)

    return finalized


def get_hosted_invoice_link(invoice_obj):
    return invoice_obj.hosted_invoice_url
