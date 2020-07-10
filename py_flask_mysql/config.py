# encoding:utf-8
import os

DEBUG = True

SECRET_KEY = os.urandom(24)

HOSTNAME = 'localhost'
PORT = '3306'
DATABASE = 'map'
USERNAME = 'root'
PASSWORD = '8520'
DB_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_COMMIT_TEARDOWN = True
BOOTSTRAP_SERVE_LOCAL = True