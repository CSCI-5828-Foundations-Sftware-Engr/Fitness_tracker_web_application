import json
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_login_success(client):
    payload = {
        "username": "admin",
        "password": "admin"
    }
    response = client.post('/login', json=payload)
    assert response.status_code == 200
    assert response.json['message'] == 'Password matched'

def test_login_fail(client):
    payload = {
        "username": "admin",
        "password": "password"
    }
    response = client.post('/login', json=payload)
    print(response.json['message'])
    assert response.status_code == 200
    assert response.json['message'] == 'Wrong password'

def test_login_user_not_found(client):
    payload = {
        "username": "adminstrator",
        "password": "password"
    }
    response = client.post('/login', json=payload)
    print(response.json['message'])
    assert response.status_code == 200
    assert response.json['message'] == 'User not found'