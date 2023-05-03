import json
import bcrypt
import pika
import smtplib
import dotenv
import os
from email.mime.text import MIMEText
import traceback

#from email.mine.text import MIMEText
from datetime import date, timedelta, datetime

from flask import Flask, request, send_from_directory, session
from flask_restful import Api
from flask_cors import CORS #comment this on deployment
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

dotenv.load_dotenv()
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

# Setting up connection parameters for RabbitMQ
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'
RABBITMQ_QUEUE_NAME = 'username'

# Configuring SMPT server
SMTP_HOST = os.environ['SMTP_HOST']
SMTP_PORT = os.environ['SMTP_PORT']
SMTP_USERNAME = os.environ['SMTP_USERNAME']
SMTP_PASSWORD = os.environ['SMTP_PASSWORD']

def send_email(to, subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = SMTP_USERNAME
    msg['To'] = to
    print(f'Line reached {message}')
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.set_debuglevel(2)
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp.send_message(msg)
        smtp.quit()

#sends an email to users
def send_email_callback(username):
    try:
        with client.start_session() as session:
            # temporarily only sending to one user
            for user in register_db.find({'username': username}):
                print(f'Creating email for user {user["username"]}')
                goal_row = goal_db.find_one({'username': user['username']})

                if not goal_row:
                    print(f'No goal rows')
                    continue

                target_weight = int(goal_row['target_weight'])
                calorie_intake_goal = int(goal_row['calorie_intake_goal'])
                calorie_burn_goal = int(goal_row['calorie_burn_goal'])
                water_goal = int(goal_row['water_goal'])
                steps_goal = int(goal_row['steps_goal'])

                # user's progress
                yesterday = datetime.now() - timedelta(days = 1)
                progress_row = nutrition_db.aggregate([
                     {'$match': {'username': user['username']}},
                     {'$lookup': {'from': 'workout', 'localField': 'date', 'foreignField': 'date', 'as': 'workout_data'}},
                     {'$unwind': '$workout_data'},
                     {'$group': {'_id': None, 'calorie_intake': {'$sum': '$calorie_intake'}, 'calorie_burn': {'$sum': '$workout_data.calorie_burn'}, 'water_intake': {'$sum': '$water_intake'}, 'total_steps': {'$sum': '$workout_data.steps'}}}
                ])#add date back in 'date': yesterday

                progress_row = list(progress_row)

                if not progress_row:
                    print(f'No progress rows')
                    continue

                calorie_burn = int(progress_row[0]['calorie_burn'])
                calorie_intake = int(progress_row[0]['calorie_intake'])
                water_intake = int(progress_row[0]['water_intake'])
                total_steps = int(progress_row[0]['total_steps'])

                # Remaining goals for the user for the day
                remaining_intake_calories = calorie_intake_goal - calorie_intake
                remaining_burn_calories = calorie_burn_goal - calorie_burn
                remaining_water = water_goal - water_intake
                remaining_steps = steps_goal - total_steps

                # Creating the email message
                message = f'Hello {user["fullname"]}, \n'
                message += f'Your goals remaining for the day are as follows:\n'
                message += f'Your remaining intake calories: {remaining_intake_calories}\n'
                message += f'Your remaining calories to be burnt: {remaining_burn_calories}\n'
                message += f'Your remaining water intake for the day: {remaining_water}\n'
                message += f'Your remaining steps for the day: {remaining_steps}\n'
                message += f'We wish you the best to complete your goals!'
                send_email(user['email'], 'Your Progress', message)
    except Exception as e:
        print(f"Error sending email: {e}")
        traceback.print_exc()

# Setting up RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue=RABBITMQ_QUEUE_NAME)

#channel._consumer_tags = set()

#Producer to send the message
def send_message(channel, message):
    channel.basic_publish(exchange='', routing_key = RABBITMQ_QUEUE_NAME, body = message)

#Consumer to fetch the message
def consume_usernames_callback(channel, method, properties, body):
    username = body.decode('utf-8')
    try:
        send_email_callback(username)
    except Exception as e:
        print(traceback.format_exc())
    channel.stop_consuming()
    #if channel._consumer_tags and len(channel._consumer_tags) == 10:
    #        channel.stop_consuming()

usernames = [user['username'] for user in register_db.find()]
for username in usernames:
    if username == 'pavit':
        send_message(channel, username)

channel.basic_consume(queue='username', on_message_callback=consume_usernames_callback, auto_ack=True)
channel.start_consuming()

#send_email_callback('pavit')