from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import stripe
from utils.auth import token_required
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
import jwt
import datetime

app = Flask(__name__)
app.config.from_object(Config)
mongo  = PyMongo(app)
stripe.api_key = app.config['STRIPE_SECRET_KEY']

#user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    mongo.db.users.insert_one({'username': data['username'], 'password': hashed_password})
    return jsonify({'message': 'User registered successfully'})

#user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = mongo.db.users.find_one({'username': data['username']})
    if user and check_password_hash(user['password', data['password']]):
        token = jwt.encode({'username': user['username'], 'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

#payment processing
@app.route('/payment', methods=['POST'])
@token_required
def payment(current_user):
    data = request.get_json()
    try:
        charge = stripe.Charge.create(
            amount = int(data['amount'])*100,
            currency='vnd',
            description=f"Payment by {current_user['username']}",
            source=data['token']
        )
        mongo.db.payments.insert_one({'user': current_user['username'], 'amount': data['amount'], 'charge_id': charge.id, 'date': datetime.datetime.utcnow()})
        return jsonify({'message': 'Payment processed successfully'})
    except stripe.error.StripeError as e:
        return jsonify({'error': str(e)}), 400
    
# service request
@app.route('/service-request', methods=['POST'])    
@token_required
def service_request(current_user):
    data = request.get_json()
    mongo.db.services.insert_one({'user': current_user['username'], 'service': data['service'], 'date': datetime.datetime.utcnow()})
    return jsonify({'message': 'Service request submitted successfully'})

# feedback submission
@app.route('/feedback', methods=['POST'])
@token_required
def feedback(current_user):
    data = request.get_json()
    mongo.db.feedback.insert_one({'user': current_user['username'], 'feedback': data['feedback'], 'date': datetime.datetime.utcnow()})
    return jsonify({'message': 'Feedback submitted successfully'})

if __name__=='__main__':
    app.run(debug=True)