# test_workout_analysis.py

from unittest.mock import MagicMock, patch
from app import app, workout_analysis

def test_workout_analysis_success():
    
    # Define the expected response data
    expected_data = {
        "target": {
            "steps_goal": "1334",
            "target_weight": "71",
            "calorie_burn_goal": "1222",
        },
        "data": [
            {
                "date": "2023-05-02",
                "total_steps": "123",
                "weight_measured": "74",
                "calories_spent": "222",
            },
            {
                "date": "2023-05-02",
                "total_steps": "01",
                "weight_measured": "284",
                "calories_spent": "10",
            },
            {
                "date": "2023-05-03",
                "total_steps": "11",
                "weight_measured": "214",
                "calories_spent": "11",
            },
        ],
    }

    # Define the expected message and status code
    expected_message = "Succesful retrieval of Workout Analysis data"
    expected_code = 200
    
    # Mock the MongoDB queries
    mock_goal_db = MagicMock()
    mock_goal_db.find_one.return_value = {
        'username': 'pavit',
        'steps_goal': 1334,
        'target_weight': 71,
        'calorie_burn_goal': 1222
    }
    mock_workout_db = MagicMock()
    mock_workout_db.find.return_value = [
        {
            'username': 'pavit',
            'date': '2023-05-02',
            'total_steps': 123,
            'weight_measured': 74,
            'calories_spent': 222
        },
        {
            'username': 'pavit',
            "date": "2023-05-02",
            "total_steps": "01",
            "weight_measured": "284",
            "calories_spent": "10",
        },
        {
            'username': 'pavit',
            "date": "2023-05-03",
            "total_steps": "11",
            "weight_measured": "214",
            "calories_spent": "11",
        }
    ]
    
    # Mock the Flask request
    with app.test_request_context('/workout_analysis', method='POST', json={"username": "pavit"}):
        # Replace the actual MongoDB queries with the mock objects
        with patch('pymongo.MongoClient') as mock_mongo:
            mock_mongo.return_value.__enter__.return_value = MagicMock()
            mock_mongo.return_value.__enter__.return_value.workout_db = mock_workout_db
            mock_mongo.return_value.__enter__.return_value.goal_db = mock_goal_db
            
            # Call the function under test
            response = workout_analysis()
            #print("RESPONSE")
            #print(response['data'])
            #print(expected_data)
            # Assert the response
            assert response['message'] == expected_message
            assert response['code'] == expected_code
            assert response['data'] == expected_data