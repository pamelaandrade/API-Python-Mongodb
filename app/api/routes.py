from flask_restful import Api

from api.user import RegisterUser, FindUserByUserName, FindUserByUserEmail, UpdateUserName, UpdateUserEmail

def create_routes(api: Api):
    
    api.add_resource(RegisterUser, '/registeruser')
    api.add_resource(FindUserByUserName, '/finduserbyusername')
    api.add_resource(FindUserByUserEmail, '/finduserbyuseremail')
    api.add_resource(UpdateUserName, '/updateusername')
    api.add_resource(UpdateUserEmail, '/updateuseremail')