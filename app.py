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
counter_signups = Counter('signups_total', 'Total number of signups')
#api.add_resource(HelloApiHandler, '/flask/hello')

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
                return {"code": 200, "message": message}

            email_found = register_db.find_one({"email": email})
            if email_found:
                message = 'This email already exists in database'
                print(message)
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

                message = 'Succesful write to register db'
                return {"code": 200, "message": message}
        else:
            message = 'Received a non-Post request'
            return {"code": 404, "message": message}
    except:
        message = "Error observed!!"
        return {"code":500, "message": message}

@app.route('/logout', methods=['post','get'])
def logout(user=""):
    #print(session)
    #session["email"]=""
    message=''
    print("Called sign out")
    try:
        if request.method == "POST":
            message = "Received post message"
            return {"code":500, "message": message}
        message = "Received non-post message"
        return {"code":500, "message": message}
    except:
        return {"code":500, "message": message}

@app.route('/', methods=['post','get'])
@app.route('/login', methods=['post','get'])
def login():
    '''
        Login page or routing for the first time
    '''
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
                    return {"code": 200, "message": message, 'username':user_found['username'], 'email':user_found['email'], 'phone':user_found['phone']}
                else:
                    message = 'Wrong password'
                    return {"code": 200, "message": message}
            else:
                message = 'User not found'
                return {"code": 404, "message": message}
        else:
            return send_from_directory(app.static_folder,'index.html')
    except:
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
                message = 'User not found'
                return {"code": 200, "message": message}
            
            # add this info to nutrition collection
            nutrition_filter = {"username":user, "date":date}
            nutrition_user_found = nutrition_db.find_one(nutrition_filter)
            if not nutrition_user_found:
                nutrition_input = {"username": user, "date": date,
                                   "calorie_intake":calorie_intake, "protein":protein, "carbs":carbs,
                                    "fat":fat,"water_intake":water_intake}
                nutrition_db.insert_one(nutrition_input)
                return {"code": 200, "message": "Succesful new user write to Nutrition db"}
            
            nutrition_new_values = {"$set": { 'date': date, 'calorie_intake': calorie_intake,
                                             'protein':protein, 'carbs':carbs,
                                             'fat':fat,'water_intake':water_intake}}
            # update collections accordingly
            nutrition_db.update_one(username_filter, nutrition_new_values)

            message = "Succesful write to Nutrition db"
            return {"code": 200, "message": message}
        else:
            message = 'Received a non-Post request'
            return {"code": 404, "message": message}
    except:
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
                return {"code": 200, "message": "Succesful new user write to Workout db"}
            
            workout_new_values = {"$set": { 'date': date, 'total_steps': total_steps,
                                           'calories_spent':calories_spent,
                                           'weight_measured':weight_measured  }}

            # update collections accordingly
            workout_db.update_one(username_filter, workout_new_values)

            message = "Succesful write to Workout db"
            return {"code": 200, "message": message}
        else:
            message = 'Received a non-Post request'
            return {"code": 404, "message": message}
    except:
        message = "Error observed!!"
        return {"code":500, "message": message}

@app.route('/goal_tracking', methods=['post','get'])
def goal_tracking():
    '''
        Profile Setup page
        goal : <id, username, target_weight, calorie_goal, water_goal, steps_goal>
    '''
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

            message = "Succesful write to Goal db"
            return {"code": 200, "message": message}
        else:
            message = 'Received a non-Post request'
            return {"code": 404, "message": message}

    except:
        message = "Error observed!!"
        return {"code":500, "message": message}
    
@app.route('/nutrition_analysis', methods=['post','get'])
def nutrition_analysis():
    '''
        target: {calories, protein, carbs, fat, water_goal}, data : {date, calories, protein, carbs, fat, water_intake} 
    '''
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

            message = "Succesful retrieval of Nutrition Analysis data"
            return {"code": 200, "message": message, "data": response_data}
        else:
            message = 'Received a non-Post request'
            return {"code": 404, "message": message}
    except:
        message = "Error observed!!"
        return {"code":500, "message": message}

@app.route('/workout_analysis', methods=['post','get'])
def workout_analysis():
    '''
        chart: id, steps, calories, weight
        target: {steps_goal, target_weight, calorie_burn_goal}, data : {date, total_steps, target_weight, calorie_burn_goal} 
    '''
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
                message = 'User not found at workout db'
                return {"code": 200, "message": message}
            
            for user_workout in user_workouts:
                print(user_workout)
                response_data['data'].append({'date' : user_workout['date'],
                                'total_steps' : user_workout['total_steps'],
                                'weight_measured' : user_workout['weight_measured'],
                                'calories_spent' : user_workout['calories_spent']})

            message = "Succesful retrieval of Workout Analysis data"
            return {"code": 200, "message": message, "data": response_data}
        else:
            message = 'Received a non-Post request'
            return {"code": 404, "message": message}
    except:
        message = "Error observed!!"
        return {"code":500, "message": message}
