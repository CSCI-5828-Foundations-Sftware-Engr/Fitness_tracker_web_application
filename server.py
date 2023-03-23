from flask import Flask, jsonify, request
from flask_cors import CORS
import hashlib, pymongo

app = Flask(__name__)
app.secret_key = "testing"
CORS(app)

# connect to MongoDB
client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
db = client['fitness_tracker']
collection = client["user_login_info"]

@app.route('/', methods=['post','get'])
@app.route('/login', methods=['post','get'])
def register():
    # get the request data
    data = request.get_json()
    # res = {"data" : {"calorie_intake": data['calorie_intake'], "calorie_burnt": data['calorie_burnt']}}
    res ={"calorie_intake": data['calorie_intake'], "calorie_burnt": data['calorie_burnt']}
    print(res)
    return res

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug = True)