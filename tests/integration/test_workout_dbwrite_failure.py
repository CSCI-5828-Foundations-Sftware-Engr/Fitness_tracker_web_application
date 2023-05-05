import json
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_workout_dbwrite_failure_user_not_found(client):
    payload = {
        "username": "dummy",
        "date" : "04/20/2023",
        "total_steps": 2130,
        "calories_spent": 610,
        "weight_measured": 60
    }
    response = client.post('/workout', json=payload)
    assert response.status_code == 200
    assert response.json['message'] == 'User not found'

def test_workout_dbwrite_failure_invalid_method(client):
    response = client.get('/workout')
    assert response.status_code == 200
    assert response.json['message'] == 'Received a non-Post request'