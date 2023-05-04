from unittest.mock import MagicMock, patch
from app import app, nutrition_analysis

def test_nutrition_success():
    # Define the expected response data
    expected_data = {
        "target": {
            "calorie_intake_goal": "2223",
            "protein_goal": "40",
            "fat_goal": "20",
            "carbs_goal": "40",
            "water_goal": "12",
        },
        "data": [
            {
                "date": "2023-05-02",
                "calorie_intake": "2241",
                "protein": "40",
                "fat": "10",
                "carbs": "50",
                "water_intake": "15",
            },
            {
                "date": "2023-05-03",
                "calorie_intake": "1241",
                "protein": "30",
                "fat": "10",
                "carbs": "60",
                "water_intake": "15",
            },
        ],
    }

    # Define the expected message and status code
    expected_message = "Succesful retrieval of Nutrition Analysis data"
    expected_code = 200
    
    # Mock the MongoDB queries
    mock_goal_db = MagicMock()
    mock_goal_db.find_one.return_value = {
        'username': 'pavit',
        'steps_goal': 1334,
        'target_weight': 71,
        'calorie_burn_goal': 1222
    }
    mock_nutrition_db = MagicMock()
    mock_nutrition_db.find.return_value = [
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
    with app.test_request_context('/nutrition_analysis', method='POST', json={"username": "pavit"}):
        # Replace the actual MongoDB queries with the mock objects
        with patch('pymongo.MongoClient') as mock_mongo:
            mock_mongo.return_value.__enter__.return_value = MagicMock()
            mock_mongo.return_value.__enter__.return_value.nutrition_db = mock_nutrition_db
            mock_mongo.return_value.__enter__.return_value.goal_db = mock_goal_db
            
            # Call the function under test
            response = nutrition_analysis()
            print("RESPONSE")
            print(response)
            print(response['data'])
            print(expected_data)
            # Assert the response
            assert response['message'] == expected_message
            assert response['code'] == expected_code
            assert response['data'] == expected_data