import json
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_register_dbretrieval_empty(client):
    payload = {
        "username": "dummy",
        "password": "password"
    }
    response = client.post('/login', json=payload)
    print(response.json['message'])
    assert response.status_code == 200
    assert response.json['message'] == 'User not found'
