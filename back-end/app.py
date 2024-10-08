from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b5b4b138050a4b559c4f369330bf94fa5807da356aa34312e1e35e941037e95d'
app.config['MONGO_URI'] = 'mongodb+srv://longnt:deankhoahocmaytinh@cluster0.fsrkk.mongodb.net/'

mongo  = PyMongo(app)

#JWT Token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = mongo.db.users.find_one({'username': data['username']})
        except:
            return jsonify({'message': 'Token is invalid'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

#User registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    mongo.db.users.insert_one({'username': data['username'], 'password': hashed_password})
    return jsonify({'message': 'User registered successfully'})

#User login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = mongo.db.users.find_one({'username': data['username']})
    if user and check_password_hash(user['password'], data['password']):
        token = jwt.encode({'username': user['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

#Payment processing (simplified)
@app.route('/payment', methods=['POST'])
@token_required
def payment(current_user):
    data = request.get_json()
    mongo.db.payments.insert_one({'user': current_user['username'], 'amount': data['amount'], 'date': datetime.datetime.utcnow()})
    return jsonify({'message': 'Payment processed successfully'})

#Service request registration
@app.route('/service-request', methods=['POST'])
@token_required
def service_request(current_user):
    data = request.get_json()
    mongo.db.services.insert_one({'user': current_user['username'],'service': data['service'], 'date': datetime.datetime.utcnow()})
    return jsonify({'message': 'Service request submitted successfully'})

#Feedback submission
@app.route('/feedback', methods=['POST'])
@token_required
def feedback(current_user):
    data = request.get_json()
    mongo.db.feedback.insert_one({'user': current_user['user'], 'feedback': data['feedback'], 'date': datetime.datetime.utcnow()})
    return jsonify({'message': 'Feedback submitted successfully'})

if __name__=='__main__':
    app.run(debug=True)