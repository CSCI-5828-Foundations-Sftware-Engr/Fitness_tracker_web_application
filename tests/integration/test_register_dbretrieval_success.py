import json
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_register_dbretrieval_success(client):
    payload = {
        "username": "admin",
        "password": "admin"
    }
    response = client.post('/login', json=payload)
    assert response.status_code == 200
    assert response.json['message'] == 'Password matched'
