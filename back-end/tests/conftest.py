import pytest
from app import app
from flask_pymongo import PyMongo
import mongomock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = "mongodb://localhost:27017/apartment_db_test"
    mongo = PyMongo(app, uri="mongomock://localhost")
    with app.test_client() as client:
        yield client