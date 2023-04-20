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