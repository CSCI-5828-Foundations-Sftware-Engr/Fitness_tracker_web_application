import json
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_nutrition_success(client):
    payload = {
        "username": "admin",
        "date" : "04/20/2023",
        "calorie_intake": 2130,
        "protein": 60,
        "carbs": 30,
        "fat": 10,
        "water_intake": 12
    }
    response = client.post('/nutrition', json=payload)
    assert response.status_code == 200
    assert response.json['message'] == 'Succesful write to Nutrition db'