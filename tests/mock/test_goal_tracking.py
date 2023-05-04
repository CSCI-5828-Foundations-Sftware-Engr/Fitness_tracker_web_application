from unittest.mock import MagicMock, patch
from app import app, goal_tracking

def test_goal_tracking_success():
    # Define the expected message and status code
    expected_message = "Succesful write to Goal db"
    expected_code = 200
    
    # Mock the MongoDB queries
    mock_goal_db = MagicMock()
    mock_goal_db.find_one.return_value = {
        'username': 'pavit',
        'steps_goal': 1334,
        'target_weight': 71,
        'calorie_burn_goal': 1222
    }
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
    with app.test_request_context('/goal_tracking', method='POST', json=payload):
        # Replace the actual MongoDB queries with the mock objects
        with patch('pymongo.MongoClient') as mock_mongo:
            mock_mongo.return_value.__enter__.return_value = MagicMock()
            mock_mongo.return_value.__enter__.return_value.goal_db = mock_goal_db
            
            # Call the function under test
            response = goal_tracking()
            #print("RESPONSE")
            #print(response)
            #print(expected_data)
            # Assert the response
            assert response['message'] == expected_message
            assert response['code'] == expected_code

def test_goal_tracking_suser_not_found():
    # Define the expected message and status code
    expected_message = "User not found"
    expected_code = 200
    
    # Mock the MongoDB queries
    mock_goal_db = MagicMock()
    payload = {
    "username": "namit",
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
    with app.test_request_context('/goal_tracking', method='POST', json=payload):
        # Replace the actual MongoDB queries with the mock objects
        with patch('pymongo.MongoClient') as mock_mongo:
            mock_mongo.return_value.__enter__.return_value = MagicMock()
            mock_mongo.return_value.__enter__.return_value.goal_db = mock_goal_db
            
            # Call the function under test
            response = goal_tracking()
            #print("RESPONSE")
            #print(response)
            #print(expected_data)
            # Assert the response
            assert response['message'] == expected_message
            assert response['code'] == expected_code

def test_goal_tracking_failure():
    # Define the expected message and status code
    expected_message = "Error observed!!"
    expected_code = 500
    
    # Mock the MongoDB queries
    mock_goal_db = MagicMock()
    mock_goal_db.find_one.return_value = {
        'username': 'pavit',
        'steps_goal': 1334,
        'target_weight': 71,
        'calorie_burn_goal': 1222
    }
    payload = {"username":"pavit","target_weight":"71","steps_goal":"1334","water_goal":"122","calorie_burn_goal":"1222","calorie_intake_goal":"1222","protein_goal":"40","carbs_goal":"40","fat_goal":"20","activity_level":"Sedentary","gender":"Male"}
    # Mock the Flask request
    with app.test_request_context('/goal_tracking', method='POST', json=payload):
        # Replace the actual MongoDB queries with the mock objects
        with patch('pymongo.MongoClient') as mock_mongo:
            mock_mongo.return_value.__enter__.return_value = MagicMock()
            mock_mongo.return_value.__enter__.return_value.goal_db = mock_goal_db
            
            # Call the function under test
            response = goal_tracking()
            #print("RESPONSE")
            #print(response)
            #print(expected_data)
            # Assert the response
            assert response['message'] == expected_message
            assert response['code'] == expected_code