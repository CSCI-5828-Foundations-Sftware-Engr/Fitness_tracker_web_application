'''
Back end code for fitness tracker application
'''
import json
import bcrypt

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
                    return {"code": 200, "message": message}
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
            if not user_goal:
                server_response_count.inc()
                workout_dbretrival_failure_count.inc()
                message = 'User not found at goal db'
                return {"code": 200, "message": message}

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