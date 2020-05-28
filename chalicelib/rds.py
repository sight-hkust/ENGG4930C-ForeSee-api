import pymysql
from pymysql import cursors, InterfaceError, OperationalError, IntegrityError
from datetime import datetime
from datetime import timedelta
import json
import re
from . import rdsconfig
import logging

# rds settings
rds_host = rdsconfig.db_endpoint
name = rdsconfig.db_username
password = rdsconfig.db_password
db_name = rdsconfig.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5,
                       cursorclass=cursors.DictCursor, charset='utf8', autocommit=True)

def query_handler(query, variables=()):
    global conn
    try:
        cur = conn.cursor()
        if query.startswith("SELECT"):
            cur.execute(query, variables)
            if query.endswith("LIMIT 1"):
                result = cur.fetchone()
                return result
            else:
                results = cur.fetchall()
                return results
        else:
            cur.execute(query, variables)
            conn.commit()
            return cur.lastrowid
    except InterfaceError as err:
        conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5,
                               cursorclass=cursors.DictCursor, charset='utf8mb4', autocommit=True)
        raise err
    except OperationalError as err:
        if err.args[0] == 2013:
            conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5,
                                   cursorclass=cursors.DictCursor, charset='utf8mb4', autocommit=True)
        raise err


def register_new_user(email, password, real_name='', phone_number='', is_parent='0'):
    result = query_handler("""INSERT INTO fs__users (email, password, real_name, phone_number, is_parent) values("%s", "%s", "%s", "%s", %s)""",
                  (email, password, real_name, phone_number, is_parent))
    return result


def login(email, password):
    result = query_handler("""SELECT email, password, real_name FROM fs__users WHERE email = %s AND password = %s LIMIT 1""", (email, password))
    if result is None:
        return False, {}
    return True, result


def add_question(email, question, sharing_data, is_private):
    result = query_handler("""INSERT INTO fs__questions(question, email, is_private, sharing_data) VALUES(%s, %s, %s, %s)""",
                         (question, email, is_private, sharing_data))
    return result


def create_record(email, password, year, month, left_eye_degree, right_eye_degree):
    result = query_handler("""SELECT id FROM fs__users WHERE email = %s AND password = %s LIMIT 1""", (email, password))
    user_id = result['id']
    result_insert = query_handler("""INSERT INTO fs__data(right_eye_myopia, left_eye_myopia, year, month, user_id)
    VALUES(%s, %s, %s, %s, %s)""", (right_eye_degree, left_eye_degree, year, month, user_id))
    return result_insert


def get_user_records(email, password):
    result = query_handler("""SELECT fs__data.* FROM fs__data, fs__users 
    WHERE fs__data.user_id = fs__users.id AND email = %s AND password = %s""", (email, password))
    return result


def get_user_doctors(email, password):
    doctors = query_handler("""SELECT doctors.email as email, doctors.id as doctor_id, doctors.phone_number as phone_number
    FROM fs__professionals as doctors, fs__users as users, fs__patient_doctor as patient_doctor
    WHERE users.email = %s AND users.password = %s 
    AND patient_doctor.user_id = users.id AND patient_doctor.doctor_id = doctors.id""", (email, password))
    return doctors


def get_all_doctors():
    doctors = query_handler("""SELECT email, id, phone_number FROM fs__professionals""")
    return doctors