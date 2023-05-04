from unittest.mock import MagicMock, patch
from app import app, login

def test_login_success():

    # Define the expected message and status code
    expected_message = "Password matched"
    expected_code = 200
    expected_email = "admin@fitongo.com"
    expected_username = "admin"
    expected_phone = "3031231111"
    
    # Mock the MongoDB queries
    mock_register_db = MagicMock()
    mock_register_db.find_one.return_value = {
        "username": "sharon",
        "fullname": "Sharon Moses",
        "email": "sh@gmail.com",
        "password": {
            "$binary": {
                "base64": "JDJiJDEyJGhzZldSYnZCWXUwQzVQSGQxdy9xTU84MWJlWlVYbjIwZHc0U2VXVkc0T0N1UHJ3M3NSTjcy",
                "subType": "00",
            }
        },
        "phone": "123"
    }  
    
    # Mock the Flask request
    with app.test_request_context('/login', method='POST', json={"username": "admin","password": "admin"}):
        # Replace the actual MongoDB queries with the mock objects
        with patch('pymongo.MongoClient') as mock_mongo:
            mock_mongo.return_value.__enter__.return_value = MagicMock()
            mock_mongo.return_value.__enter__.return_value.mock_register_db = mock_register_db
            
            # Call the function under test
            response = login()
            #print("RESPONSE")
            #print(response)
            #print(expected_data)
            # Assert the response
            assert response['message'] == expected_message
            assert response['code'] == expected_code
            assert response['username'] == expected_username
            assert response['email'] == expected_email
            assert response['phone'] == expected_phone
