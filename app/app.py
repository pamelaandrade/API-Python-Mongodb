from flask import Flask, app
from flask_restful import Api
from pymongo import MongoClient
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager

from api.routes import create_routes

import os

client = MongoClient("mongodb://db:27017")
db = client.MoneyManagementDB
usersbooks = db["UsersBsooks"]

def get_flask_app() -> app.Flask:
    flask_app = Flask(__name__)
    api = Api(app=flask_app)
    create_routes(api=api)
    return flask_app

if __name__ == '__main__':
    app = get_flask_app()
    app.run(debug=False, host='0.0.0.0')
