from unittest.mock import MagicMock, patch
from app import app, signup

def test_signup_failure():
    # Define the expected message and status code
    expected_message = "There already is a user by that name"
    expected_code = 200
    
    # Mock the MongoDB queries
    mock_register_db = MagicMock()
    mock_register_db.find.return_value = [
        {
            'username': 'pavit',
            "fullname": "adminstrator",
            "email": "admin@fitongo.com",
            "password": "password",
            "contactNumber": "3031231111"
        }
    ]
    payload = {
        "username": "admin",
        "fullname": "adminstrator",
        "email": "admin@fitongo.com",
        "password": "password",
        "contactNumber": "3031231111"
    }
    # Mock the Flask request
    with app.test_request_context('/signup', method='POST', json=payload):
        # Replace the actual MongoDB queries with the mock objects
        with patch('pymongo.MongoClient') as mock_mongo:
            mock_mongo.return_value.__enter__.return_value = MagicMock()
            mock_mongo.return_value.__enter__.return_value.register_db = mock_register_db
            
            # Call the function under test
            response = signup()
            print("RESPONSE")
            print(response)
            # Assert the response
            assert response['message'] == expected_message
            assert response['code'] == expected_code