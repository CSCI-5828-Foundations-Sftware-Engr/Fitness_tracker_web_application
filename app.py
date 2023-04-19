from flask import Flask, jsonify, request, send_from_directory
from flask_restful import Api, Resource, reqparse

from flask_cors import CORS #comment this on deployment
from api.HelloApiHandler import HelloApiHandler
import json

app = Flask(__name__, static_url_path='', static_folder='fitness-tracker-react/build')
api = Api(app)

@app.route("/", methods=['post','get'])
@app.route("/login", methods=['post','get'])
def login():
    if request.method == "POST":
        # get the request data
        print(request)
        data = request.get_json()
        print(json.dumps(data, indent=4))
        # res = {"data" : {"calorie_intake": data['calorie_intake'], "calorie_burnt": data['calorie_burnt']}}
        res ={"calorie_intake": data['calorie_intake'], "calorie_burnt": data['calorie_burnt']}
        print(res)
        return res
    else:
        return send_from_directory(app.static_folder,'index.html')

api.add_resource(HelloApiHandler, '/flask/hello')

@app.route('/signup', methods=['post','get'])
def signup():
    message=''

    try:
        if request.method == "POST":
            fullname = request.form.get("name")
            user = request.form.get("username")
            email = request.form.get("email")
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")
            address = request.form.get("address")
            country = request.form.get("country")
            phone = request.form.get("phone")

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
                messa:ge = 'This email already exists in database'
                print(message)
                #return render_template('pages-register.html', message=message)
                #return send_from_directory(app.static_folder,'index.html')

            if password1 != password2:
                message = 'Passwords should match! Try again'
                print(message)
                #return render_template('pages-register.html', message=message)
                #return send_from_directory(app.static_folder,'index.html')
            else:
                hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
                user_input = {'name': user, 'email': email, 'password': hashed, 'fullname': fullname, 'country':country, 'address':address, 'phone':phone }
                print(user_input)

                #records.insert_one(user_input)
                # New User, push the document to user_info collection
                session['email'] = email

                #return render_template('index.html', user=user_input)
                #return send_from_directory(app.static_folder,'index.html')

        #return render_template('pages-register.html')
        #return send_from_directory(app.static_folder,'index.html')
    except:
        #return render_template('error.html')
        #return send_from_directory(app.static_folder,'index.html')

@app.route('/', methods=['post','get'])
@app.route('/login', methods=['post','get'])
def login():
    message=''
    print("Called login")
'''
    print(session)
    if "email" in session and session["email"]!="":
        js_string = create_graph()
        print(js_string)
        recent_info=[]
        time_now = datetime.now().strftime(fmt)
        jobs = list(db.recent_info.find({"time":{'$lt':time_now}}).limit(10).sort('time', -1))
        for job in jobs:
            print(job["text"])
            recent_activity = {}
            recent_activity["time"] = delta_to_string(datetime.now() - datetime.strptime(job["time"], fmt))
            recent_activity["text"] = job["text"]
            recent_info.append(recent_activity)
        user_found = records.find_one({"email": session["email"]})
        user = {'name': user_found["name"], 'email': user_found["email"], 'password': user_found["password"], 'fullname': user_found["fullname"], 'country': user_found["country"], 'address':user_found["address"], 'phone':user_found["phone"] }
        print(user)
        return render_template('index.html', user=user, js=js_string, recents=recent_info)
'''
    try:
        if request.method == "POST":
            user = request.form.get("username")
            password = request.form.get("password")
            # get the user document from user_info collection
            #user_found = records.find_one({"name": user})
            if user_found:
                passwordcheck = user_found['password']
                if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                    print("Password matched")
                    session["email"] = user_found["email"]
                    user = {'name': user_found["name"], 'email': user_found["email"], 'password': user_found["password"], 'fullname': user_found["fullname"], 'country': user_found["country"], 'address':user_found["address"], 'phone':user_found["phone"] }
                    js_string = create_graph()
                    recent_info=[]
                    time_now = datetime.now().strftime(fmt)
                    jobs = list(db.recent_info.find({"time":{'$lt':time_now}}).limit(10).sort('time', -1))
                    for job in jobs:
                        print(job["text"])
                        recent_activity = {}
                        recent_activity["time"] = delta_to_string(datetime.now() - datetime.strptime(job["time"], fmt))
                        recent_activity["text"] = job["text"]
                        recent_info.append(recent_activity)
                    return render_template('index.html', user=user, js=js_string, recents=recent_info)
                   #return send_from_directory(app.static_folder,'index.html')
                else:
                    if "email" in session:
                        user_found = records.find_one({"email": session["email"]})
                        user = {'name': user_found["name"], 'email': user_found["email"], 'password': user_found["password"], 'fullname': user_found["fullname"], 'country': user_found["country"], 'address':user_found["address"], 'phone':user_found["phone"] }
                        print("else case")
                        session["email"] = user_found["email"]
                        return render_template('index.html', user=user)
                    message = 'Wrong password'
                    print("Wrong password")
                    #return render_template('pages-login.html', message=message)
                    #return send_from_directory(app.static_folder,'index.html')
            else:
                message = 'User found'
                #return render_template('pages-login.html', message=message)
                #return send_from_directory(app.static_folder,'index.html')
        #return render_template('pages-login.html')
        #return send_from_directory(app.static_folder,'index.html')
    except:
        #return render_template('error.html', message="Error found, please check and login again")
        #return send_from_directory(app.static_folder,'index.html')
