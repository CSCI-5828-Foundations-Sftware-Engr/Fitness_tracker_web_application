import json
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_signup_success(client):
    payload = {
        "username": "johndoe",
        "fullname": "John Doe",
        "email": "johndoe@example.com",
        "password": "password",
        "contactNumber": "1234567890"
    }
    response = client.post('/signup', json=payload)
    assert response.status_code == 200
    assert response.json['message'] == 'Succesful write to register db'

def test_signup_duplicate_user(client):
    payload = {
        "username": "admin",
        "fullname": "adminstrator",
        "email": "admin@fitongo.com",
        "password": "password",
        "contactNumber": "3031231111"
    }
    response = client.post('/signup', json=payload)
    assert response.status_code == 200
    assert response.json['message'] == 'There already is a user by that name'

def test_signup_duplicate_email(client):
    payload = {
        "username": "adminstrator",
        "fullname": "adminstrator",
        "email": "admin@fitongo.com",
        "password": "password",
        "contactNumber": "3031231111"
    }
    response = client.post('/signup', json=payload)
    assert response.status_code == 200
    assert response.json['message'] == 'This email already exists in database'

def test_signup_invalid_method(client):
    response = client.get('/signup')
    assert response.status_code == 200
    assert response.json['message'] == 'Received a non-Post request'