# import stripe
# from dotenv import load_dotenv
# import os
# import logging
#
# load_dotenv()
#
# # Replace with your own secret key
# stripe.api_key = os.getenv('STRIPE_API_KEY')
#
# # Choose the customer's country here (change as needed)
# # Options: "GB" (UK), "US", "CA", "SA", "AE"
# # country_code = "GB"  # ← Change this line to "US", "CA", "SA", or "AE"
# # currency = {
# #     "GB": "gbp",
# #     "US": "usd",
# #     "CA": "cad",
# #     "SA": "sar",
# #     "AE": "aed"
# # }[country_code]
#
# # 1. Create the customer
# customer = stripe.Customer.create(
#     name="Acme Ltd",
#     email="khermz2012@gmail.com",  # Stripe will email the invoice here
#     # address={
#     # "line1": "123 Business Street",
#     # "city": {
#     #     "GB": "London",
#     #     "US": "New York",
#     #     "CA": "Toronto",
#     #     "SA": "Riyadh",
#     #     "AE": "Dubai"
#     # }[country_code],
#     # "postal_code": {
#     #     "GB": "SW1A 1AA",
#     #     "US": "10001",
#     #     "CA": "M5V 2T6",
#     #     "SA": "12271",
#     #     "AE": "00000"
#     # }[country_code],
#     # "country": country_code,
#     # },
#     description=f"Test customer",
# )
#
# print(f"Customer created: {customer.id}")
#
# # 2. Create an invoice payable ONLY by bank transfer
# invoice = stripe.Invoice.create(
#     customer=customer.id,
#     collection_method="send_invoice",  # customer pays manually
#     # days_until_due=14,
#     auto_advance=False,
#     description="Annual Service – Payable by Bank Transfer",
#     payment_settings={
#         "payment_method_types": ["ach_debit",
#                                  "acss_debit",
#                                  "card",
#                                  "crypto",
#                                  # "au_becs_debit", AUD
#                                  # "bacs_debit", GBP
#                                  # "customer_balance",
#                                  # "pay_by_bank", GBP
#                                  "us_bank_account"],  # cards will be hidden
#     },
#     currency="usd",
# )
# #
# # 3. Add a line item (example £999.00 / $999.00 etc.)
# stripe.InvoiceItem.create(
#     customer=customer.id,
#     amount=49900,  # 999.00 in the smallest currency unit
#     currency="usd",
#     description="Annual Hosting & Support 2026",
# )
#
# # 4. Finalize → this generates the virtual bank account / reference number
# invoice = stripe.Invoice.finalize_invoice(invoice.id)
#
# # 5. Send the invoice (Stripe emails the customer automatically)
# # stripe.Invoice.send_invoice(invoice.id)
#
# print(f"Invoice created and emailed!")
# print(f"Hosted invoice URL: {invoice.hosted_invoice_url}")
# # print(f"Download PDF: {invoice.invoice_pdf}")
# # print(f"Amount due: {invoice.amount_due / 100:.2f} {currency.upper()}")
