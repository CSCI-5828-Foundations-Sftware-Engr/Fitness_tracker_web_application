from flask import Flask, jsonify, request, send_from_directory
from flask_restful import Api, Resource, reqparse

from flask_cors import CORS #comment this on deployment
from api.HelloApiHandler import HelloApiHandler
import json

app = Flask(__name__, static_url_path='', static_folder='fitness-tracker-react/build')
api = Api(app)

@app.route("/", methods=['post','get'])
@app.route("/login", methods=['post','get'])
def register():
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

# connect to MongoDB
# client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
# db = client['fitness_tracker']
# collection = client["user_login_info"]

# @app.route('/', methods=['post','get'])
# @app.route('/login', methods=['post','get'])
# def register():
#     # get the request data
#     print(request)
#     data = request.get_json()
#     print(json.dumps(data, indent=4))
#     # res = {"data" : {"calorie_intake": data['calorie_intake'], "calorie_burnt": data['calorie_burnt']}}
#     res ={"calorie_intake": data['calorie_intake'], "calorie_burnt": data['calorie_burnt']}
#     print(res)
#     return res

# if __name__ == '__main__':
#     app.run(host="0.0.0.0", debug = True)