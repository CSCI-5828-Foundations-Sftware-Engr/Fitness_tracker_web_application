import json
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_goal_db_write_success(client):
    payload = {
    "username": "pavit",
    "current_weight": "79",
    "age": "21",
    "height":"180",
    "target_weight": "71",
    "steps_goal": "1334",
    "water_goal": "12",
    "calorie_burn_goal": "1222",
    "calorie_intake_goal": "2223",
    "protein_goal": "40",
    "carbs_goal": "40",
    "fat_goal": "20",
    "activity_level": "Sedentary",
    "gender": "Male"
    }
    response = client.post('/goal_tracking', json=payload)
    assert response.status_code == 200
    assert response.json['message'] == 'Succesful write to Goal db'
