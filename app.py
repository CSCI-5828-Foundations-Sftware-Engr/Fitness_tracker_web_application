from flask import Flask, jsonify, request, send_from_directory, render_template, session
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
import bcrypt, json, queue
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from api.HelloApiHandler import HelloApiHandler

app = Flask(__name__, static_url_path='', static_folder='fitness-tracker-react/build')
CORS(app)
api = Api(app)

api.add_resource(HelloApiHandler, '/flask/hello')

# Setting up the mongo driver
#client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
uri = "mongodb+srv://fitness:fitness@cluster0.rzau3x9.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.get_database('user_info')
records = db.register

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
            user_found = records.find_one({"name": user})
            email_found = records.find_one({"email": email})
            print(user)

            if user_found:
                message = 'There already is a user by that name'
                print(message)

            if email_found:
                message = 'This email already exists in database'
                print(message)
            else:
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                user_input = {'username': user, 'fullname': fullname, 'email': email, 'password': hashed, 'phone':phone}
                print(user_input)

                records.insert_one(user_input)
    except:
        print("Error observed!!")

# login page or routing for the first time
def login_first():
    if request.method == "POST":
        # get the request data
        print(request)
        data = request.get_json()
        print(json.dumps(data, indent=4))
    else:
        return send_from_directory(app.static_folder,'index.html')

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
            user_found = records.find_one({"username": user})
            if user_found:
                passwordcheck = user_found['password']
                if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                    print("Password matched")
                else:
                    message = 'Wrong password'
                    print("Wrong password")
            else:
                message = 'User found'
                print("User not found")
    except:
        print("Error observed!!")
