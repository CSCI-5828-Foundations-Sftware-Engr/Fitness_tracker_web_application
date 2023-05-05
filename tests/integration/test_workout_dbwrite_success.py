import json
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_workout_dbwrite_success(client):
    payload = {
        "username": "admin",
        "date" : "04/20/2023",
        "total_steps": 2130,
        "calories_spent": 610,
        "weight_measured": 60
    }
    response = client.post('/workout', json=payload)
    assert response.status_code == 200
    assert response.json['message'] == 'Succesful write to Workout db'