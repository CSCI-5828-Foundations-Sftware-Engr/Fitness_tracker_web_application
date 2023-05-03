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














# import unittest
# from unittest.mock import patch, Mock
# from app import app

# class TestWorkoutAnalysis(unittest.TestCase):
#     @patch('flask.request')
#     @patch('pymongo.collection.Collection.find_one')
#     @patch('pymongo.collection.Collection.find')
#     def test_workout_analysis_with_valid_data(self, mock_find, mock_find_one, mock_request):
#         # Create a mock request object with valid JSON data
#         mock_request.method = 'POST'
#         mock_request.get_json.return_value = {
#             'username': 'testuser'
#         }

#         # Create a mock user goal object
#         mock_user_goal = {
#             '_id': '123',
#             'username': 'testuser',
#             'steps_goal': 10000,
#             'target_weight': 70,
#             'calorie_burn_goal': 2000
#         }

#         # Create a mock user workout object
#         mock_user_workout = {
#             '_id': '456',
#             'username': 'testuser',
#             'date': '2022-05-01',
#             'total_steps': 5000,
#             'weight_measured': 75,
#             'calories_spent': 1000
#         }

#         # Set up the mock find_one method to return the mock user goal object
#         mock_find_one.return_value = mock_user_goal

#         # Set up the mock find method to return a list with the mock user workout object
#         mock_find.return_value = [mock_user_workout]

#         # Call the workout_analysis function
#         with app.test_client() as client:
#             response = client.post('/workout_analysis', json={'username': 'testuser'})

#         # Assert that the response has status code 200 and expected message and data
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json['message'], 'Succesful retrieval of Workout Analysis data')
#         self.assertEqual(response.json['data']['target']['steps_goal'], 10000)
#         self.assertEqual(response.json['data']['target']['target_weight'], 70)
#         self.assertEqual(response.json['data']['target']['calorie_burn_goal'], 2000)
#         self.assertEqual(len(response.json['data']['data']), 1)
#         self.assertEqual(response.json['data']['data'][0]['date'], '2022-05-01')
#         self.assertEqual(response.json['data']['data'][0]['total_steps'], 5000)
#         self.assertEqual(response.json['data']['data'][0]['weight_measured'], 75)
#         self.assertEqual(response.json['data']['data'][0]['calories_spent'], 1000)
        
#         # Assert that the expected database calls were made
#         mock_request.get_json.assert_called_once()
#         mock_find_one.assert_called_once_with({'username': 'testuser'})
#         mock_find.assert_called_once_with({'username': 'testuser'})

# from unittest import TestCase
# from flask import Flask, request
# from unittest.mock import Mock
# from app import app

# class TestApplication(TestCase):

#     def test_get_user(self):
#         # Create a mock object for the database connection.
#         db_connection = Mock()

#         # Create a mock object for the `get_user_from_database()` function.
#         get_user_function = Mock()
#         get_user_function.return_value = {
#             "username": "johndoe",
#             "fullname": "John Doe",
#             "email": "johndoe@example.com",
#             "password": "password"
#         }

#         # Create a Flask application.
#         app = Flask(__name__)

#         # Register the `workout_analysis()` function with the Flask application.
#         app.add_url_rule("/workout_analysis", "workout_analysis", iter(get_user_function))

#         # Create a test client for the Flask application.
#         client = app.test_client()

#         # Make a request to the `/workout_analysis` endpoint.
#         response = client.get("/workout_analysis")

#         # Assert that the response status code is 200.
#         self.assertEqual(response.status_code, 200)

#         # Assert that the response content is the JSON representation of the user.
#         self.assertEqual(response.content, b'{"username": "johndoe", "fullname": "John Doe", "email": "johndoe@example.com", "password": "password"}')


# # import unittest
# # from unittest.mock import patch, Mock
# # from app import app

# # class TestWorkoutAnalysis(unittest.TestCase):
# #     @patch('flask.request')
# #     def test_workout_analysis_with_valid_data(self, mock_request):
# #         # Create a mock request object with valid JSON data
# #         mock_request.get_json.return_value = {
# #             'username': 'pavit',
# #             'steps_goal': 10000,
# #             'target_weight': 70,
# #             'calorie_burn_goal': 2000
# #         }

# #         # Call the workout_analysis function
# #         with app.test_client() as client:
# #             response = client.post('/workout_analysis', json={"username": "pavit"})

# #             # Assert that the response has status code 200 and expected message and data
# #             self.assertEqual(response.status_code, 200)
# #             self.assertEqual(response.json['message'], 'Succesful retrieval of Workout Analysis data')
# #             self.assertEqual(response.json['data']['target']['steps_goal'], 10000)
# #             self.assertEqual(response.json['data']['target']['target_weight'], 70)
# #             self.assertEqual(response.json['data']['target']['calorie_burn_goal'], 2000)
# #             self.assertEqual(len(response.json['data']['data']), 2)
            
# #             # Assert that the expected database calls were made
# #             mock_request.get_json.assert_called_once()
