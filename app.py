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
            # password2 =  data["password2"]
            phone =   data["contactNumber"]

            # check the user and email in the documents of user_info collection from MongoDB
            user_found = records.find_one({"name": user})
            email_found = records.find_one({"email": email})
            print(user)

            if user_found:
                message = 'There already is a user by that name'
                print(message)
                #return render_template('pages-register.html', message=message)
                #return send_from_directory(app.static_folder,'index.html')

            if email_found:
                message = 'This email already exists in database'
                print(message)
                #return render_template('pages-register.html', message=message)
                #return send_from_directory(app.static_folder,'index.html')

            # if password1 != password2:
                # message = 'Passwords should match! Try again'
                # print(message)
                #return render_template('pages-register.html', message=message)
                #return send_from_directory(app.static_folder,'index.html')
            else:
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                user_input = {'username': user, 'fullname': fullname, 'email': email, 'password': hashed, 'phone':phone}
                print(user_input)

                records.insert_one(user_input)
                # New User, push the document to user_info collection
                # session['email'] = email

                #return render_template('index.html', user=user_input)
                #return send_from_directory(app.static_folder,'index.html')

        #return render_template('pages-register.html')
        #return send_from_directory(app.static_folder,'index.html')
    except:
        print("Error observed!!")
        # return render_template('error.html')
        #return send_from_directory(app.static_folder,'index.html')

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
    # print(session)
    # if "email" in session and session["email"]!="":
    #     js_string = create_graph()
    #     print(js_string)
    #     recent_info=[]
    #     time_now = datetime.now().strftime(fmt)
    #     jobs = list(db.recent_info.find({"time":{'$lt':time_now}}).limit(10).sort('time', -1))
    #     for job in jobs:
    #         print(job["text"])
    #         recent_activity = {}
    #         recent_activity["time"] = delta_to_string(datetime.now() - datetime.strptime(job["time"], fmt))
    #         recent_activity["text"] = job["text"]
    #         recent_info.append(recent_activity)
    #     user_found = records.find_one({"email": session["email"]})
    #     user = {'name': user_found["name"], 'email': user_found["email"], 'password': user_found["password"], 'fullname': user_found["fullname"], 'country': user_found["country"], 'address':user_found["address"], 'phone':user_found["phone"] }
    #     print(user)
    #     return render_template('index.html', user=user, js=js_string, recents=recent_info)
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
                    # session["email"] = user_found["email"]
                    # user = {'username': user_found["name"], 'email': user_found["email"], 'password': user_found["password"], 'fullname': user_found["fullname"], 'country': user_found["country"], 'address':user_found["address"], 'phone':user_found["phone"] }
                    # js_string = create_graph()
                    # recent_info=[]
                    # time_now = datetime.now().strftime(fmt)
                    # jobs = list(db.recent_info.find({"time":{'$lt':time_now}}).limit(10).sort('time', -1))
                    # for job in jobs:
                    #     print(job["text"])
                    #     recent_activity = {}
                    #     recent_activity["time"] = delta_to_string(datetime.now() - datetime.strptime(job["time"], fmt))
                    #     recent_activity["text"] = job["text"]
                    #     recent_info.append(recent_activity)
                    # return render_template('index.html', user=user, js=js_string, recents=recent_info)
                   #return send_from_directory(app.static_folder,'index.html')
                else:
                    # if "email" in session:
                    #     user_found = records.find_one({"email": session["email"]})
                    #     user = {'name': user_found["name"], 'email': user_found["email"], 'password': user_found["password"], 'fullname': user_found["fullname"], 'country': user_found["country"], 'address':user_found["address"], 'phone':user_found["phone"] }
                    #     print("else case")
                    #     session["email"] = user_found["email"]
                    #     return render_template('index.html', user=user)
                    message = 'Wrong password'
                    print("Wrong password")
                    #return render_template('pages-login.html', message=message)
                    #return send_from_directory(app.static_folder,'index.html')
            else:
                message = 'User found'
                print("User not found")
                #return render_template('pages-login.html', message=message)
                #return send_from_directory(app.static_folder,'index.html')
        #return render_template('pages-login.html')
        #return send_from_directory(app.static_folder,'index.html')
    except:
        print("Error observed!!")
        #return render_template('error.html', message="Error found, please check and login again")
        #return send_from_directory(app.static_folder,'index.html')
