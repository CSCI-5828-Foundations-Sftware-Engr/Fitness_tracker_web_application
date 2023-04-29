from flask import Flask, jsonify, request, send_from_directory, render_template, session
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
import bcrypt, json, queue
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#from api.HelloApiHandler import HelloApiHandler

app = Flask(__name__, static_url_path='', static_folder='fitness-tracker-react/build')
CORS(app)
api = Api(app)

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
uri = "mongodb+srv://fitness:fitness@cluster0.rzau3x9.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.get_database('user_info')
register = db.register
nutrition = db.nutrition
workout = db.workout
goal = db.goal

# login page or routing for the first time
def login_first():
    if request.method == "POST":
        # get the request data
        print(request)
        data = request.get_json()
        print(json.dumps(data, indent=4))
    else:
        return send_from_directory(app.static_folder,'index.html')

@app.route('/signup', methods=['post','get'])
def signup():
    message=''
    try:
        if request.method == "POST":
            data = request.get_json()
            print(json.dumps(data, indent=4))

            user = data["username"]
            fullname = data["fullname"]
            email = data["email"]
            password =  data["password"]
            phone =   data["contactNumber"]

            # check the user and email in the documents of user_info collection from MongoDB
            user_found = register.find_one({"username": user})            
            if user_found:
                message = 'There already is a user by that name'
                print(message)
                return {"code": 200, "message": message}

            email_found = register.find_one({"email": email})
            if email_found:
                message = 'This email already exists in database'
                print(message)
                return {"code": 200, "message": message}
            else:
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                user_input = {'username': user, 'fullname': fullname, 'email': email, 'password': hashed, 'phone':phone}
                print(user_input)

                register.insert_one(user_input)
                message = 'Succesful write to register db'
                return {"code": 200, "message": message}
        else:
            message = 'Received a non-Post request'
            return {"code": 404, "message": message}
    except:
        message = "Error observed!!"
        return {"code":500, "message": message}

@app.route('/', methods=['post','get'])
@app.route('/login', methods=['post','get'])
def login():
    message=''
    print("Called login")
    try:
        if request.method == "POST":
            data = request.get_json()
            print(json.dumps(data, indent=4), session)

            user = data["username"]
            password =  data["password"]

            # get the user document from user_info collection
            user_found = register.find_one({"username": user})
            if user_found:
                passwordcheck = user_found['password']
                if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                    message = "Password matched"
                    return {"code": 200, "message": message}
                else:
                    message = 'Wrong password'
                    return {"code": 200, "message": message}
            else:
                message = 'User not found'
                return {"code": 404, "message": message}
        else:
            message = 'Received a non-Post request'
            return {"code": 404, "message": message}
    except:
        message = "Error observed!!"
        return {"code":500, "message": message}

# Nutrition Log form
# nutrition : <id, username, date, calorie_intake, Protein(%), Carbs(%), Fat(%)>     #
@app.route('/nutrition', methods=['post','get'])
def nutrition():
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
            user_found = nutrition.find_one({"username": user})
            if not user_found:
                message = 'User not found'
                return {"code": 200, "message": message}
            
            # add this info to workout collection
            filter = {"username":user}
            nutrition_new_values = {"$set": { 'date': date, 'calorie_intake': calorie_intake, 'protein':protein, 'carbs':carbs, 'fat':fat,'water_intake':water_intake }}

            # update collections accordingly
            nutrition.update_one(filter, nutrition_new_values)

            message = "Succesful write to Nutrition db"
            return {"code": 200, "message": message}
        else:
            message = 'Received a non-Post request'
            return {"code": 404, "message": message}
    except:
        message = "Error observed!!"
        return {"code":500, "message": message}

# Workout Log form
# workout   : <id, username, date, total_steps, calories_spent, weight_measured>
@app.route('/workout', methods=['post','get'])
def workout():
    message = ""
    try:
        if request.method == "POST":
            data = request.get_json()
            print(json.dumps(data, indent=4), session)

            # user check
            user_found = workout.find_one({"username": user})
            if not user_found:
                message = 'User not found'
                return {"code": 200, "message": message}

            user = data["username"]
            date = data["date"]
            total_steps = data["total_steps"]
            calories_spent = data["calories_spent"]
            weight_measured = data["weight_measured"]
            
            # add this info to workout collection
            filter = {"username":user}
            workout_new_values = {"$set": { 'date': date, 'total_steps': total_steps, 'calories_spent':calories_spent, 'weight_measured':weight_measured  }}

            # update collections accordingly
            workout.update_one(filter, workout_new_values)

            message = "Succesful write to Workout db"
            return {"code": 200, "message": message}
        else:
            message = 'Received a non-Post request'
            return {"code": 404, "message": message}

    except:
        message = "Error observed!!"
        return {"code":500, "message": message}

# Profile Setup page
# goal : <id, username, target_weight, calorie_goal, water_goal, steps_goal>
@app.route('/goal_tracking', methods=['post','get'])
def goal_tracking():
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
            filter = {"username":user}
            register_new_values = {"$set": { 'current_weight': current_weight, 'age': age, 'height':height }}
            goal_new_values = {"$set": { 'target_weight': target_weight, 'steps_goal': steps_goal, 'water_goal':water_goal, 'calorie_burn_goal':calorie_burn_goal, 'calorie_intake_goal':calorie_intake_goal,'protein_goal':protein_goal,'carbs_goal':carbs_goal, 'fat_goal':fat_goal}}

            # update collections accordingly
            register.update_one(filter, register_new_values)
            goal.update_one(filter, goal_new_values)

            message = "Succesful write to Goal db"
            return {"code": 200, "message": message}
        else:
            message = 'Received a non-Post request'
            return {"code": 404, "message": message}

    except:
        message = "Error observed!!"
        return {"code":500, "message": message}
    
# target: {calories, protein, carbs, fat, water_goal}, data : {date, calories, protein, carbs, fat, water_intake} 
def nutrition_analysis():
    message = ""
    try:
        if request.method == "POST":
            data = request.get_json()
            print(json.dumps(data, indent=4), session)

            user = data['username']
            
            # add current weight, age and height to register || other info to goal 
            response_data = {}
            response_data['target'] = {}
            response_data['data'] = {}

            # return the target data
            user_goal = goal.find_one({'username': user})
            response_data['target']['calorie_intake_goal'] = user_goal['calorie_intake_goal']
            response_data['target']['protein_goal'] = user_goal['protein_goal']
            response_data['target']['fat_goal'] = user_goal['fat_goal']
            response_data['target']['carbs_goal'] = user_goal['carbs_goal']
            response_data['target']['water_goal'] = user_goal['water_goal']

            # return the current data
            user_nutrition = nutrition.find_one({'username': user})
            response_data['data']['calorie_intake'] = user_nutrition['calorie_intake']
            response_data['data']['protein'] = user_goal['protein']
            response_data['data']['fat'] = user_goal['fat']
            response_data['data']['carbs'] = user_goal['carbs']
            response_data['data']['water_intake'] = user_goal['water_intake']

            message = "Succesful retrieval of Nutrition Analysis data"
            return {"code": 200, "message": message, "data": response_data}
        else:
            message = 'Received a non-Post request'
            return {"code": 404, "message": message}

    except:
        message = "Error observed!!"
        return {"code":500, "message": message}

# chart: id, steps, calories, weight
def workout_analysis():
    message = ""
    try:
        if request.method == "POST":
            data = request.get_json()
            print(json.dumps(data, indent=4), session)

            user = data['username']
            
            # add current weight, age and height to register || other info to goal 
            response_data = {}
            response_data['target'] = {}
            response_data['data'] = {}

            # return the target data
            user_goal = goal.find_one({'username': user})
            response_data['target']['steps_goal'] = user_goal['steps_goal']
            response_data['target']['target_weight'] = user_goal['target_weight']
            response_data['target']['calorie_burn_goal'] = user_goal['calorie_burn_goal']

            # return the current data
            user_nutrition = workout.find_one({'username': user})
            response_data['data']['total_steps'] = user_nutrition['total_steps']
            response_data['data']['weight_measured'] = user_goal['weight_measured']
            response_data['data']['calories_spent'] = user_goal['calories_spent']

            message = "Succesful retrieval of Workout Analysis data"
            return {"code": 200, "message": message, "data": response_data}
        else:
            message = 'Received a non-Post request'
            return {"code": 404, "message": message}

    except:
        message = "Error observed!!"
        return {"code":500, "message": message}
