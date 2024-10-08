import stripe
from flask import jsonify
import stripe.error

def process_payment(amount, token):
    try:
        charge = stripe.Charge.create(
            amount=amount * 100,
            currency='vnd',
            source=token
        )
        return jsonify({'status': 'success', 'charge_id': charge.id})
    except stripe.error.StripeError as e:
        return jsonify({'status': 'error', 'message': str(e)})