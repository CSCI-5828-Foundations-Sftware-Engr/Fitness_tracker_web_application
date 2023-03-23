from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import hashlib

app = Flask(__name__)
CORS(app)

# connect to MongoDB
client = MongoClient()
db = client['data_base_name']
collection = client["user_info"]

@app.route('/register', methods=['POST'])
def register():
    # get the request data
    data = request.get_json()

    # hash the password
    password_hash = hashlib.sha256(data['password'].encode()).hexdigest()

    # insert the user into the database
    result = db.users.insert_one({
        'email': data['email'],
        'password': password_hash
    })

    # return the user ID
    return jsonify({'user_id': str(result.inserted_id)})

if __name__ == '_main_':
    app.run()