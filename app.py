from chalice import Chalice
from chalicelib import rds
import random
from urllib.parse import urlparse, parse_qs

app = Chalice(app_name='ForeSeeApi')


# Helper Functions
def parse_post_parameters(raw_data):
    i_parsed_data = parse_qs(raw_data)
    parsed_data = {}
    for key in i_parsed_data:
        parsed_data[key] = i_parsed_data[key][0]

    return parsed_data


@app.route('/')
def index():
    i = random.randint(0, 1)
    if i == 1:
        return {'status': 'OK', 'message': 'My name is Charon, I carry information through the internet river.'}
    else:
        return {'status': 'OK',
                'message': 'Do you know the Trainman from Matrix? He is my uncle.'}


@app.route('/parse_test', methods=['POST'], content_types=['application/x-www-form-urlencoded'])
def parse_test():
    parsed = parse_post_parameters(app.current_request.raw_body.decode())
    return {
        'status': 'OK',
        'parsed_data': parsed
    }


@app.route('/create_user', methods=['POST'], content_types=['application/json'], cors=True)
def create_user():
    parsed = app.current_request.json_body
    email = parsed['email']
    password = parsed['password']
    #birthday = parsed['birthday']
    real_name = parsed['real_name']
    phone_number = parsed['phone_number']
    is_parent = parsed['is_parent']
    user = rds.register_new_user(email, password, real_name, phone_number, is_parent)
    return {'status': 'OK', 'user': user}


@app.route('/login', methods=['POST'], content_types=['application/json'], cors=True)
def login():
    parsed = app.current_request.json_body
    email = parsed['email']
    password = parsed['password']
    status, user = rds.login(email, password)
    if not status:
        return {'status':'err'}
    return {'status': 'OK', 'user': user}


@app.route('/add_question', methods=['POST'], content_types=['application/json'], cors=True)
def add_question():
    parsed = app.current_request.json_body
    email = parsed['email']
    question = parsed['question']
    sharing_data = parsed['sharing_data']
    is_private = parsed['is_private']
    result = rds.add_question(email, question, sharing_data, is_private)
    return {'status': 'OK'}


@app.route('/create_record', methods=['POST'], content_types=['application/json'], cors=True)
def create_record():
    parsed = app.current_request.json_body
    email = parsed['email']
    password = parsed['password']
    left_eye_degree = parsed['left_eye_degree']
    right_eye_degree = parsed['right_eye_degree']
    year = parsed['year']
    month = parsed['month']
    result = rds.create_record(email, password, year, month, left_eye_degree, right_eye_degree)
    return {'status': 'OK', 'result': result}


@app.route('/get_user_records', methods=['GET'], cors=True)
def get_user_records():
    params = app.current_request.query_params
    email = params['email']
    password = params['password']
    records = rds.get_user_records(email, password)
    return {'status': 'OK', 'records': records}


@app.route('/get_user_doctors', methods=['GET'], cors=True)
def get_user_doctors():
    params = app.current_request.query_params
    email = params['email']
    password = params['password']
    doctors = rds.get_user_doctors(email, password)
    return {'status': 'OK', 'doctors': doctors}


@app.route('/get_all_doctors', methods=['GET'], cors=True)
def get_all_doctors():
    doctors = rds.get_all_doctors()
    return {'status': 'OK', 'doctors': doctors}