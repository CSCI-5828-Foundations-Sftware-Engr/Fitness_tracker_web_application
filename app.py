'''
Back end code for fitness tracker application
'''
from datetime import time
import json
import bcrypt
import requests

from flask import Flask, Response, request, send_from_directory, session
from flask_restful import Api
from flask_cors import CORS #comment this on deployment
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from prometheus_client import Counter
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
#from api.HelloApiHandler import HelloApiHandler

app = Flask(__name__, static_url_path='', static_folder='fitness-tracker-react/build')
app.debug = True
CORS(app)
api = Api(app)
#api.add_resource(HelloApiHandler, '/flask/hello')

#################################################################################################
#                                  Metrics for Prometheus                                       #
#################################################################################################
counter_signups = Counter('signups_total', 'Total number of signups')
counter_logins = Counter('logins_total', 'Total number of logins')
#server_request_latency = Histogram('server_request_latency', 'Latency of server requests', ['method', 'endpoint'])
#Request and Response
server_request_count = Counter('server_request_count', 'Total number of requests made to the backend server')
server_response_count = Counter('server_response_count', 'Total number of responses sent from the backend server')
#signups
signup_success_count = Counter('signup_success_count', 'Total number of successful requests made to the backend server for signup endpoint')
signup_failure_count = Counter('signup_failure_count', 'Total number of failure requests made to the backend server for signup endpoint')
signup_error_count = Counter('signup_error_count', 'Total number of error requests made to the backend server for signup endpoint')
#logins
login_success_count = Counter('login_success_count', 'Total number of successful requests made to the backend server for login endpoint')
login_failure_count = Counter('login_failure_count', 'Total number of failure requests made to the backend server for login endpoint')
login_error_count = Counter('login_error_count', 'Total number of error requests made to the backend server for login endpoint')
#nutrition
nutrition_dbwrite_success_count = Counter('nutrition_dbwrite_success_count', 'Total number of successful requests made to the backend server for nutrition endpoint')
nutrition_dbwrite_failure_count = Counter('nutrition_dbwrite_failure_count', 'Total number of failure requests made to the backend server for nutrition endpoint')
nutrition_dbwrite_error_count = Counter('nutrition_dbwrite_error_count', 'Total number of error requests made to the backend server for nutrition endpoint')
#workout
workout_dbwrite_success_count = Counter('workout_dbwrite_success_count', 'Total number of successful requests made to the backend server for workout endpoint')
workout_dbwrite_failure_count = Counter('workout_dbwrite_failure_count', 'Total number of failure requests made to the backend server for workout endpoint')
workout_dbwrite_error_count = Counter('workout_dbwrite_error_count', 'Total number of error requests made to the backend server for workout endpoint')
#goal tracking
goal_tracking_dbwrite_success_count = Counter('goal_tracking_dbwrite_success_count', 'Total number of successful requests made to the backend server for goal_tracking endpoint')
goal_tracking_dbwrite_failure_count = Counter('goal_tracking_dbwrite_failure_count', 'Total number of failure requests made to the backend server for goal_tracking endpoint')
goal_tracking_dbwrite_error_count = Counter('goal_tracking_dbwrite_error_count', 'Total number of error requests made to the backend server for goal_tracking endpoint')
#nutrition_analysis
nutrition_dbretrival_success_count = Counter('nutrition_dbretrival_success_count', 'Total number of successful requests made to the backend server for nutrition_analysis endpoint')
nutrition_dbretrival_failure_count = Counter('nutrition_dbretrival_failure_count', 'Total number of failure requests made to the backend server for nutrition_analysis endpoint')
nutrition_dbretrival_error_count = Counter('nutrition_dbretrival_error_count', 'Total number of error requests made to the backend server for nutrition_analysis endpoint')
#workout_analysis
workout_dbretrival_success_count = Counter('workout_dbretrival_success_count', 'Total number of successful requests made to the backend server for workout_analysis endpoint')
workout_dbretrival_failure_count = Counter('workout_dbretrival_failure_count', 'Total number of failure requests made to the backend server for workout_analysis endpoint')
workout_dbretrival_error_count = Counter('workout_dbretrival_error_count', 'Total number of error requests made to the backend server for workout_analysis endpoint')


#################################################################################################
#                                             Schema                                            #
# register  : <id, username, fullname, email, password, contactNumber, Age, Weight>             #
# goal      : <id, username, target_weight, calorie_goal, water_goal, steps_goal>               #
# nutrition : <id, username, date, calorie_intake, Protein(%), Carbs(%), Fat(%), water_intake>  #
# workout   : <id, username, date, total_steps, calories_spent, weight_measured>                #
#################################################################################################

# Setting up the mongo driver
#client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
URI = "mongodb+srv://fitness:fitness@cluster0.rzau3x9.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(URI, server_api=ServerApi('1'))
db = client.get_database('user_info')
register_db = db.register
nutrition_db = db.nutrition
workout_db = db.workout
goal_db = db.goal
diet_db = db.diet
reco_db = db.recommendations

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

def login_first():
    '''
        login page or routing for the first time
    '''
    if request.method == "POST":
        # get the request data
        print(request)
        data = request.get_json()
        print(json.dumps(data, indent=4))
        return data
    else:
        return send_from_directory(app.static_folder,'index.html')

@app.route('/signup', methods=['post','get'])
def signup():
    '''
        Signup page or routing for the first time
    '''
    server_request_count.inc()
    message=''
    try:
        if request.method == "POST":
            data = request.get_json()
            print(json.dumps(data, indent=4))

            user = data["username"]
            email = data["email"]
            password = data["password"]
            phone = data["contactNumber"]

            # check the user and email in the documents of user_info collection from MongoDB
            user_found = register_db.find_one({"username": user})
            if user_found:
                message = 'There already is a user by that name'
                print(message)
                signup_failure_count.inc()
                server_response_count.inc()
                return {"code": 200, "message": message}

            email_found = register_db.find_one({"email": email})
            if email_found:
                message = 'This email already exists in database'
                print(message)
                signup_failure_count.inc()
                server_response_count.inc()
                return {"code": 200, "message": message}
            else:
                hashed = bcrypt.hashpw(password.encode('utf-8'),
                                       bcrypt.gensalt())
                user_input = {'username': user, 'email': email,
                              'password': hashed, 'phone':phone}
                print(user_input)

                register_db.insert_one(user_input)
                counter_signups.inc()
                #print(counter_signups)
                # Get the current value of the counter
                counter_value = counter_signups._value.get()
                print(f"Current value of counter: {counter_value}")
                server_response_count.inc()
                message = 'Succesful write to register db'
                return {"code": 200, "message": message}
        else:
            signup_failure_count.inc()
            server_response_count.inc()
            message = 'Received a non-Post request'
            return {"code": 404, "message": message}
    except:
        signup_error_count.inc()
        server_response_count.inc()
        message = "Error observed!!"
        return {"code":500, "message": message}

@app.route('/logout', methods=['post','get'])
def logout(user=""):
    #print(session)
    #session["email"]=""
    server_request_count.inc()
    message=''
    print("Called sign out")
    try:
        if request.method == "POST":
            server_response_count.inc()
            message = "Received post message"
            return {"code":500, "message": message}
        server_response_count.inc()
        message = "Received non-post message"
        return {"code":500, "message": message}
    except:
        server_response_count.inc()
        return {"code":500, "message": message}

@app.route('/', methods=['post','get'])
@app.route('/login', methods=['post','get'])
def login():
    '''
        Login page or routing for the first time
    '''
    server_request_count.inc()
    message=''
    print("Called login")
    try:
        if request.method == "POST":
            data = request.get_json()
            print(json.dumps(data, indent=4), session)

            user = data["username"]
            password =  data["password"]

            # get the user document from user_info collection
            user_found = register_db.find_one({"username": user})
            if user_found:
                passwordcheck = user_found['password']
                if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                    message = "Password matched"
                    counter_logins.inc()
                    counter_value = counter_logins._value.get()
                    print(f"Current value of counter: {counter_value}")
                    login_success_count.inc()
                    server_response_count.inc()
                    return {"code": 200, "message": message, 'username':user_found['username'], 'email':user_found['email'], 'phone':user_found['phone']}
                else:
                    login_failure_count.inc()
                    server_response_count.inc()
                    message = 'Wrong password'
                    return {"code": 200, "message": message}
            else:
                login_failure_count.inc()
                server_response_count.inc()
                message = 'User not found'
                return {"code": 404, "message": message}
        else:
            server_response_count.inc()
            return send_from_directory(app.static_folder,'index.html')
    except:
        login_error_count.inc()
        server_response_count.inc()
        message = "Error observed!!"
        return {"code":500, "message": message}

@app.route('/nutrition', methods=['post','get'])
def nutrition():
    '''
        Nutrition Log form
        nutrition : <id, username, date, calorie_intake, water_intake, Protein(%), Carbs(%), Fat(%)>
        eg: {
            "username": "pavit",
            "date": "2023-05-01",
            "calorie_intake":"3241",
            "protein":"40",
            "carbs":"40",
            "fat":"20",
            "water_intake":"5"
            }
    '''
    server_request_count.inc()
    # Get the current value of the counter
    counter_value = server_request_count._value.get()
    print(f"Current value of server_request_count: {counter_value}")
    message = ""
    try:
        if request.method == "POST":
            data = request.get_json()
            print(json.dumps(data, indent=4), session)
            user = data["username"]
            date = data["date"]
            calorie_intake = data["calorie_intake"]
            protein = data["protein"]
            carbs = data["carbs"]
            fat = data["fat"]
            water_intake = data['water_intake']
            
            # user check
            username_filter = {"username":user}
            user_found = register_db.find_one(username_filter)
            if not user_found:
                server_response_count.inc()
                nutrition_dbwrite_failure_count.inc()
                message = 'User not found'
                return {"code": 200, "message": message}
            
            # add this info to nutrition collection
            nutrition_filter = {"username":user, "date":date}
            nutrition_user_found = nutrition_db.find_one(nutrition_filter)
            print(nutrition_user_found)
            if not nutrition_user_found:
                nutrition_input = {"username": user, "date": date,
                                   "calorie_intake":calorie_intake, "protein":protein, "carbs":carbs,
                                    "fat":fat,"water_intake":water_intake}
                nutrition_db.insert_one(nutrition_input)
                server_response_count.inc()
                nutrition_dbwrite_success_count.inc()
                return {"code": 200, "message": "Succesful new user write to Nutrition db"}

            nutrition_new_values = {"$set": { 'date': date, 'calorie_intake': calorie_intake,
                                             'protein':protein, 'carbs':carbs,
                                             'fat':fat,'water_intake':water_intake}}
            # update collections accordingly
            nutrition_db.update_one(username_filter, nutrition_new_values)
            server_response_count.inc()
            nutrition_dbwrite_success_count.inc()
            message = "Succesful write to Nutrition db"

            return {"code": 200, "message": message}
        else:
            server_response_count.inc()
            nutrition_dbwrite_failure_count.inc()
            message = 'Received a non-Post request'
            return {"code": 404, "message": message}
    except:
        server_response_count.inc()
        nutrition_dbwrite_error_count.inc()
        message = "Error observed!!"
        return {"code":500, "message": message}

@app.route('/workout', methods=['post','get'])
def workout():
    ''' 
        Workout Log form
        workout   : <id, username, date, total_steps, calories_spent, weight_measured>
        eg: {
            "username": "pavit",
            "date": "2023-05-01",
            "total_steps":"2312",
            "calories_spent":"1232",
            "weight_measured":"183"
            }
    '''
    server_request_count.inc()
    message = ""
    try:
        if request.method == "POST":
            data = request.get_json()
            print(json.dumps(data, indent=4), session)

            user = data["username"]
            date = data["date"]
            total_steps = data["total_steps"]
            calories_spent = data["calories_spent"]
            weight_measured = data["weight_measured"]
            
            # user check
            username_filter = {"username":user}
            user_found = register_db.find_one(username_filter)
            if not user_found:
                server_response_count.inc()
                workout_dbwrite_failure_count.inc()
                message = 'User not found'
                return {"code": 200, "message": message}
            
            # add this info to workout collection
            workout_filter = {"username":user, "date":date}
            workout_user_found = workout_db.find_one(workout_filter)
            if not workout_user_found:
                workout_input = {"username": user, "date": date,
                                   "total_steps":total_steps, "calories_spent":calories_spent,
                                   "weight_measured":weight_measured}
                workout_db.insert_one(workout_input)
                workout_dbwrite_success_count.inc()
                server_response_count.inc()
                return {"code": 200, "message": "Succesful new user write to Workout db"}
            
            workout_new_values = {"$set": { 'date': date, 'total_steps': total_steps,
                                           'calories_spent':calories_spent,
                                           'weight_measured':weight_measured  }}

            # update collections accordingly
            workout_db.update_one(username_filter, workout_new_values)
            server_response_count.inc()
            workout_dbwrite_success_count.inc()
            # Get the current value of the counter
            counter_value = server_response_count._value.get()
            print(f"Current value of server_response_count: {counter_value}")
            counter_value = workout_dbwrite_success_count._value.get()
            print(f"Current value of workout_dbwrite_success_count: {counter_value}")
            counter_value = server_request_count._value.get()
            print(f"Current value of server_request_count: {counter_value}")
            message = "Succesful write to Workout db"
            return {"code": 200, "message": message}
        else:
            server_response_count.inc()
            workout_dbwrite_failure_count.inc()
            message = 'Received a non-Post request'
            return {"code": 404, "message": message}
    except:
        server_response_count.inc()
        workout_dbwrite_error_count.inc()
        message = "Error observed!!"
        return {"code":500, "message": message}

@app.route('/goal_tracking', methods=['post','get'])
def goal_tracking():
    '''
        Profile Setup page
        goal : <id, username, target_weight, calorie_goal, water_goal, steps_goal>
    '''
    server_request_count.inc()
    message = ""
    try:
        if request.method == "POST":
            data = request.get_json()
            print(json.dumps(data, indent=4), session)

            user = data["username"]
            current_weight = data["current_weight"]
            age = data["age"]
            height = data["height"]
            target_weight = data["target_weight"]
            steps_goal = data["steps_goal"]
            water_goal = data["water_goal"]
            calorie_intake_goal = data["calorie_intake_goal"]
            calorie_burn_goal = data["calorie_burn_goal"]
            protein_goal = data["protein_goal"]
            carbs_goal = data["carbs_goal"]
            fat_goal = data["fat_goal"]
            
            # add current weight, age and height to register || other info to goal 
            username_filter = {"username":user}
            register_new_values = {"$set": { 'current_weight': current_weight, 'age': age, 'height':height }}
            
            # user check
            user_found = register_db.find_one(username_filter)
            if not user_found:
                server_response_count.inc()
                goal_tracking_dbwrite_failure_count.inc()
                message = 'User not found'
                return {"code": 200, "message": message}
            
            # add this info to workout collection
            goal_user_found = goal_db.find_one(username_filter)
            if not goal_user_found:
                goal_input = {  'username':user,
                                'target_weight': target_weight,
                                'steps_goal': steps_goal,
                                'water_goal':water_goal,
                                'calorie_burn_goal':calorie_burn_goal,
                                'calorie_intake_goal':calorie_intake_goal,
                                'protein_goal':protein_goal,
                                'carbs_goal':carbs_goal,
                                'fat_goal':fat_goal
                            } 
                goal_db.insert_one(goal_input)
                server_response_count.inc()
                goal_tracking_dbwrite_success_count.inc()
                return {"code": 200, "message": "Succesful new user write to Goal db"}            

            # update collections accordingly
            goal_new_values = {"$set": { 'target_weight': target_weight,
                                        'steps_goal': steps_goal,
                                        'water_goal':water_goal,
                                        'calorie_burn_goal':calorie_burn_goal,
                                        'calorie_intake_goal':calorie_intake_goal,
                                        'protein_goal':protein_goal,
                                        'carbs_goal':carbs_goal,
                                        'fat_goal':fat_goal
                                        }
                                }
            
            register_db.update_one(username_filter, register_new_values)
            goal_db.update_one(username_filter, goal_new_values)
            server_response_count.inc()
            goal_tracking_dbwrite_success_count.inc()
            message = "Succesful write to Goal db"
            return {"code": 200, "message": message}
        else:
            server_response_count.inc()
            goal_tracking_dbwrite_failure_count.inc()
            message = 'Received a non-Post request'
            return {"code": 404, "message": message}

    except:
        server_response_count.inc()
        goal_tracking_dbwrite_error_count.inc()
        message = "Error observed!!"
        return {"code":500, "message": message}
    
@app.route('/nutrition_analysis', methods=['post','get'])
def nutrition_analysis():
    '''
        target: {calories, protein, carbs, fat, water_goal}, data : {date, calories, protein, carbs, fat, water_intake} 
    '''
    server_request_count.inc()
    message = ""
    try:
        if request.method == "POST":
            data = request.get_json()
            print(json.dumps(data, indent=4), session)

            user = data['username']
            
            # add current weight, age and height to register || other info to goal 
            response_data = {'target':{}, 'data':[]}

            # return the target data
            user_goal = goal_db.find_one({'username': user})
            if not user_goal:
                server_response_count.inc()
                nutrition_dbretrival_failure_count.inc()
                message = 'User not found at goal db'
                return {"code": 200, "message": message}
            
            print(user_goal)
            response_data['target']['calorie_intake_goal'] = user_goal['calorie_intake_goal']
            response_data['target']['protein_goal'] = user_goal['protein_goal']
            response_data['target']['fat_goal'] = user_goal['fat_goal']
            response_data['target']['carbs_goal'] = user_goal['carbs_goal']
            response_data['target']['water_goal'] = user_goal['water_goal']

            # return the current data
            user_nutritions = list(nutrition_db.find({'username': user}))
            if len(user_nutritions) == 0:
                server_response_count.inc()
                nutrition_dbretrival_failure_count.inc()
                message = 'User not found at nutrition db'
                return {"code": 200, "message": message}
            
            print(user_nutritions)
            response_data['data'] = []
            for user_nutrition in user_nutritions:
                response_data['data'].append({'date' : user_nutrition['date'],
                                'calorie_intake' : user_nutrition['calorie_intake'],
                                'protein' : user_nutrition['protein'],
                                'fat' : user_nutrition['fat'],
                                'carbs' : user_nutrition['carbs'],
                                'water_intake' : user_nutrition['water_intake']})
            print("Reached here!!")
            server_response_count.inc()
            nutrition_dbretrival_success_count.inc()
            message = "Succesful retrieval of Nutrition Analysis data"
            return {"code": 200, "message": message, "data": response_data}
        else:
            server_response_count.inc()
            nutrition_dbretrival_failure_count.inc()
            message = 'Received a non-Post request'
            return {"code": 404, "message": message}
    except:
        server_response_count.inc()
        nutrition_dbretrival_error_count.inc()
        message = "Error observed!!"
        return {"code":500, "message": message}

@app.route('/workout_analysis', methods=['post','get'])
def workout_analysis():
    '''
        chart: id, steps, calories, weight
        target: {steps_goal, target_weight, calorie_burn_goal}, data : {date, total_steps, target_weight, calorie_burn_goal} 
    '''
    server_request_count.inc()
    message = ""
    try:
        if request.method == "POST":
            data = request.get_json()
            print(json.dumps(data, indent=4), session)

            user = data['username']
            
            # add current weight, age and height to register || other info to goal 
            response_data = {'target':{}, 'data':[]}

            # return the target data
            user_goal = goal_db.find_one({'username': user})
            response_data['target']['steps_goal'] = user_goal['steps_goal']
            response_data['target']['target_weight'] = user_goal['target_weight']
            response_data['target']['calorie_burn_goal'] = user_goal['calorie_burn_goal']

            # return the current data
            user_workouts = list(workout_db.find({'username': user}))
            if len(user_workouts) == 0:
                server_response_count.inc()
                workout_dbretrival_failure_count.inc()
                message = 'User not found at workout db'
                return {"code": 200, "message": message}
            
            for user_workout in user_workouts:
                print(user_workout)
                response_data['data'].append({'date' : user_workout['date'],
                                'total_steps' : user_workout['total_steps'],
                                'weight_measured' : user_workout['weight_measured'],
                                'calories_spent' : user_workout['calories_spent']})
            server_response_count.inc()
            workout_dbretrival_success_count.inc()
            message = "Succesful retrieval of Workout Analysis data"
            return {"code": 200, "message": message, "data": response_data}
        else:
            server_response_count.inc()
            workout_dbretrival_failure_count.inc()
            message = 'Received a non-Post request'
            return {"code": 404, "message": message}
    except:
        server_response_count.inc()
        workout_dbretrival_error_count.inc()
        message = "Error observed!!"
        return {"code":500, "message": message}

def calculate_bmr(weight, height, age, gender):
    if gender.lower() == "male":
        bmr = 66 + (13.75 * weight) + (5 * height) - (6.75 * age)
    else:
        bmr = 655 + (9.56 * weight) + (1.85 * height) - (4.68 * age)
    return bmr

# timeframe in days, weight in kgs, height in cms
def calculate_ideal_calorie_intake(weight, target_weight, activity_level="sedentary", gender="male", age=22, height=180):
    print("Called Ideal")
    time_frame = 30
    height_in_meters = height / 100  # Convert height from centimeters to meters
    bmr = calculate_bmr(weight, height_in_meters, age, gender)
    
    if target_weight < weight:
        calorie_deficit = (weight - target_weight) * 7700 / time_frame  # Each kilogram is approximately 7700 calories
        ideal_calorie_intake = bmr - calorie_deficit
    else:
        calorie_surplus = (target_weight - weight) * 7700 / time_frame
        ideal_calorie_intake = bmr + calorie_surplus

    activity_level_multipliers = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extra active": 1.9
    }

    ideal_calorie_intake *= activity_level_multipliers.get(activity_level.lower(), 1.2)
    return ideal_calorie_intake

@app.route('/recommendations', methods=['post','get'])
def recommendations():
    '''
        called on demand by user fetches recepies and suggests the ideal weight, ideal water intake, ideal calories intake
    '''
    message = ""
    try:
        if request.method == "POST":
            data = request.get_json()
            print(json.dumps(data, indent=4), session)

            user = data['username']

            # fetch from the reco db the average values 
            reco_entry = reco_db.find_one({"username": user})
            goal_entry = goal_db.find_one({"username": user})
            register_entry = register_db.find_one({"username": user})
            response_data = {'high_protein':[], 'low_fat':[], 'low_carbs':[], 'balanced':[]}
            print(register_entry, goal_entry, reco_entry)
            response_data['ideal_calorie_intake'] = calculate_ideal_calorie_intake(int(register_entry['current_weight']), int(goal_entry['target_weight']), goal_entry['activity_level'], goal_entry['gender'], int(register_entry['age']), int(register_entry['height']))

            if reco_entry["average_protein"] < int(goal_entry["protein_goal"]):
                response_data["high_protein"] = list(diet_db.find_one({'diet':'high_protein'})['recipes'])
            if reco_entry["average_fat"] > int(goal_entry["fat_goal"]):
                response_data["low_fat"] = list(diet_db.find_one({'diet':'low_fat'})['recipes'])
            if reco_entry["average_carbs"] > int(goal_entry["carbs_goal"]):
                response_data["low_carbs"] = list(diet_db.find_one({'diet':'low_carbs'})['recipes'])
            response_data["balanced"] = list(diet_db.find_one({'diet':'balanced'})['recipes'])

            print(response_data)
            message = "Succesful retrieval of Workout Analysis data"
            return {"code": 200, "message": message, 'response':response_data}
        else:
            message = 'Received a non-Post request'
            return {"code": 404, "message": message}
    except:
        message = "Error observed!!"
        return {"code":500, "message": message}

@app.route('/data_collector', methods=['post','get'])
def data_collector():
    '''
        called by the cron job and this API does:
        1. Fetch the latest recepies for tags: high-protein, low-fat, low-carb, balanced
        2. Calculate the average of all users and identify the ones with those that don't meet the expectations and update reco db
    '''
    message = ""
    try:
        if request.method == "POST":
            # Fetch the latest recepies for tags: high-protein, low-fat, low-calorie
            high_protein_url = 'https://api.edamam.com/api/recipes/v2?type=public&app_id=b6fb901b&app_key=%2082bcdf1e491ca4822f768e796dc1d4de&diet=high-protein&cuisineType=American&imageSize=SMALL&random=true'
            balanced_url = 'https://api.edamam.com/api/recipes/v2?type=public&app_id=b6fb901b&app_key=%2082bcdf1e491ca4822f768e796dc1d4de&diet=balanced&cuisineType=American&imageSize=SMALL&random=true'
            low_carbs_url = 'https://api.edamam.com/api/recipes/v2?type=public&app_id=b6fb901b&app_key=%2082bcdf1e491ca4822f768e796dc1d4de&diet=low-carb&cuisineType=American&imageSize=SMALL&random=true'
            low_fat_url = 'https://api.edamam.com/api/recipes/v2?type=public&app_id=b6fb901b&app_key=%2082bcdf1e491ca4822f768e796dc1d4de&diet=low-fat&cuisineType=American&imageSize=SMALL&random=true'

            # Fetch the high protein diet and store in db
            print("Fetching High Protein diet")
            response = requests.get(high_protein_url)
            if response.status_code == 200:
                data = response.json()
                json_unformatted_data = data['hits'][:5]

                json_data = []
                # trim json to fit the data
                for json_unformatted_var in list(json_unformatted_data):
                    json_var = {}
                    json_var["url"] = json_unformatted_var["recipe"]["url"]
                    json_var["image"] = json_unformatted_var["recipe"]["image"]
                    json_var["label"] = json_unformatted_var["recipe"]["label"]
                    json_data.append(json_var)
                
                # print(json_data)
                if len(json_data) != 0:
                    high_protein_diet_entry_found = diet_db.find_one({"diet":"high_protein"})
                    if not high_protein_diet_entry_found:
                        high_protein_diet = {"diet":"high_protein", 'recipes': json_data[:5]}
                        diet_db.insert_one(high_protein_diet)
                    else:
                        reco_input = {"$set": {'recipes':  json_data[:5]}}
                        diet_db.update_one({"diet":"high_protein"}, reco_input)                        
            else:
                return {"code": 200, "message": 'High Protein diet fetch request failed with status code:'+response.status_code}

            # Fetch the high protein diet and store in db
            print("Fetching Balanced diet")
            # time.sleep(10)
            response = requests.get(balanced_url)
            if response.status_code == 200:
                data = response.json()
                json_unformatted_data = data['hits'][:5]

                json_data = []
                # trim json to fit the data
                for json_unformatted_var in list(json_unformatted_data):
                    json_var = {}
                    json_var["url"] = json_unformatted_var["recipe"]["url"]
                    json_var["image"] = json_unformatted_var["recipe"]["image"]
                    json_var["label"] = json_unformatted_var["recipe"]["label"]
                    json_data.append(json_var)
                
                # print(json_data)
                if len(json_data) != 0:
                    balanced_diet_entry_found = diet_db.find_one({"diet":"balanced"})
                    if not balanced_diet_entry_found:
                        balanced_diet = {"diet":"balanced", 'recipes': json_data[:5]}
                        diet_db.insert_one(balanced_diet)
                    else:
                        reco_input = {"$set": {'recipes': json_data[:5]}}
                        diet_db.update_one({"diet":"balanced"}, reco_input)
            else:
                return {"code": 200, "message": 'Balanced diet fetch request failed with status code:'+response.status_code}

            # Fetch the high protein diet and store in db
            print("Fetching Low carb diet")
            # time.sleep(10)
            response = requests.get(low_carbs_url)
            if response.status_code == 200:
                data = response.json()
                json_unformatted_data = data['hits'][:5]

                json_data = []
                # trim json to fit the data
                for json_unformatted_var in list(json_unformatted_data):
                    json_var = {}
                    json_var["url"] = json_unformatted_var["recipe"]["url"]
                    json_var["image"] = json_unformatted_var["recipe"]["image"]
                    json_var["label"] = json_unformatted_var["recipe"]["label"]
                    json_data.append(json_var)
                
                # print(json_data)
                if len(json_data) != 0:
                    low_carbs_diet_entry_found = diet_db.find_one({"diet":"low_carbs"})
                    if not low_carbs_diet_entry_found:
                        low_carbs_diet = {"diet":"low_carbs", 'recipes': json_data[:5]}
                        diet_db.insert_one(low_carbs_diet)
                    else:
                        reco_input = {"$set": {'recipes': json_data[:5]}}
                        diet_db.update_one({"diet":"low_carbs"}, reco_input)
            else:
                return {"code": 200, "message": 'Low carb diet fetch request failed with status code:'+response.status_code}

            # Fetch the high protein diet and store in db
            print("Fetching Low fat diet")
            # time.sleep(10)
            response = requests.get(low_fat_url)
            if response.status_code == 200:
                data = response.json()
                json_unformatted_data = data['hits'][:5]

                json_data = []
                # trim json to fit the data
                for json_unformatted_var in list(json_unformatted_data):
                    json_var = {}
                    json_var["url"] = json_unformatted_var["recipe"]["url"]
                    json_var["image"] = json_unformatted_var["recipe"]["image"]
                    json_var["label"] = json_unformatted_var["recipe"]["label"]
                    json_data.append(json_var)
                
                # print(json_data)
                if len(json_data) != 0:
                    low_fat_diet_entry_found = diet_db.find_one({"diet":"low_fat"})
                    if not low_fat_diet_entry_found:
                        low_fat_diet = {"diet":"low_fat", 'recipes': json_data[:5]}
                        diet_db.insert_one(low_fat_diet)
                    else:
                        reco_input = {"$set": {'recipes': json_data[:5]}}
                        diet_db.update_one({"diet":"low_fat"}, reco_input)
            else:
                return {"code": 200, "message": 'Low fat diet fetch request failed with status code:'+response.status_code}
            
            # Calculate the average of all users and update reco db
            users = register_db.find()
            for user in users:
                user_nutritions = list(nutrition_db.find({'username': user['username']}))
                if len(user_nutritions) == 0:
                    continue
                
                sum_protein = 0
                cnt_protein = 0
                sum_carb = 0
                cnt_carb = 0
                sum_fat = 0
                cnt_fat = 0
                for n in user_nutritions:
                    cnt_protein += 1
                    sum_protein += int(n["protein"])
                    cnt_carb += 1
                    sum_carb += int(n["carbs"])
                    cnt_fat += 1
                    sum_fat += int(n["fat"])
                
                # print(user['username'], sum_protein, sum_fat, sum_carb, cnt_fat, cnt_carb, cnt_protein)
                reco_user_found = reco_db.find_one({'username':user['username']})
                if not reco_user_found:
                    reco_input = {"username":user['username'], "average_protein": sum_protein/cnt_protein, "average_fat":sum_fat/cnt_fat, "average_carbs":sum_carb/cnt_carb}
                    # print(reco_input)
                    reco_db.insert_one(reco_input)
                else:
                    reco_entry = {"$set": {"average_protein":int(sum_protein/cnt_protein), "average_fat":int(sum_fat/cnt_fat), "average_carbs":int(sum_carb/cnt_carb)}}
                    reco_db.update_one({'username': user['username']}, reco_entry)
                    # print("Updated")

            message = "Succesful write to recommendations db"
            return {"code": 200, "message": message}
        else:
            message = 'Received a non-Post request'
            return {"code": 404, "message": message}
    except:
        message = "Error observed!!"
        return {"code":500, "message": message}