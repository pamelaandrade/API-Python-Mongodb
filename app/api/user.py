from pymongo import MongoClient
from flask import Flask, jsonify, request
from flask_restful import Api
from flask_restful import Resource
import bcrypt


app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.MoneyManagementDB
usersbooks = db["UsersBsooks"]

def generateReturnDictionary(status, msg):
        retJson = {
            "status": status,
            "msg": msg
        }
        return retJson

def UserExist(username):
    if usersbooks.find({"username":username}).count() == 0:
        return False
    else:
        return True

def UserExistEmail(email):
    if usersbooks.find({"email":email}).count() == 0:
        return False
    else:
        return True

def emailUser(username):
    email = usersbooks.find({
        "username":username
    })[0]["email"]
    return email

def nameUser(email):
    username = usersbooks.find({
        "email":email
    })[0]["username"]
    return username

def verifyPw(username, password):
    hashed_pw = usersbooks.find({
        "username":username
    })[0]["password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def verifyCredentialsUsername(username, password):
    if not UserExist(username):
        return generateReturnDictionary(301, "Invalid Username"), True

    correct_pw = verifyPw(username, password)

    if not correct_pw:
        return generateReturnDictionary(302, "Incorrect Password"), True

    return None, False

def verifyCredentialsEmail(email, password):
    if not UserExistEmail(email):
        return generateReturnDictionary(304, "Invalid email"), True

    correct_pw = verifyPw(email, password)

    if not correct_pw:
        return generateReturnDictionary(302, "Incorrect Password"), True

    return None, False

class RegisterUser(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        email    = postedData["email"]

        if UserExist(username):
            return generateReturnDictionary(301, "Invalid Username")

        if UserExistEmail(email):
            return generateReturnDictionary(304, "Invalid email")
        
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        usersbooks.insert({
            "username": username,
            "password": hashed_pw,
            "email"   : email
        })
        return jsonify(generateReturnDictionary(200, "You successfully signed up for the API"))

class FindUserByUserName(Resource):
    def get(self):
        postedData = request.get_json()

        username = postedData["username"]

        if not UserExist(username):
            return generateReturnDictionary(301, "Invalid Username")
        else:
            email = emailUser(username)
            retJson = {
                "status": 200,
                "username": username,
                "email": email
            }
            return jsonify({'result':retJson})

class FindUserByUserEmail(Resource):
    def get(self):
        postedData = request.get_json()

        email = postedData["email"]

        if not UserExistEmail(email):
            return generateReturnDictionary(304, "Invalid email")
        else:
            username = nameUser(email)
            retJson = {
                "status": 200,
                "username": username,
                "email": email
            }
            return jsonify({'result':retJson})

class UpdateUserName(Resource):
    def post(self):
        postedData = request.get_json()

        email = postedData["email"]
        password = postedData["password"] 
        newusername = postedData["newusername"]   

        if not UserExistEmail(email):
            return generateReturnDictionary(304, "Invalid email")
        else: 
            usersbooks.update({
                "email": email
            },{
                "$set":{
                    "username": newusername,
                }
            })
            return generateReturnDictionary(202, "Username updated with successfully")

class UpdateUserEmail(Resource):
    def post(self):
        postedData = request.get_json()

        newemail = postedData["newemail"]
        password = postedData["password"] 
        username = postedData["username"]   

        if not UserExist(username):
            return generateReturnDictionary(301, "Invalid Username")
        else: 
            usersbooks.update({
                "username": username
            },{
                "$set":{
                    "email": newemail,
                }
            })
            return generateReturnDictionary(202, "Email updated with successfully")
