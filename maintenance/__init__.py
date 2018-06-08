from flask import Flask
from flask_restful import Api

from maintenance.Request import HelloWorld, RequestApi, RequestService
from maintenance.User import UserRegister
from maintenance.User import UserLogin



app = Flask(__name__)
api = Api(app)
"""my api resources """
api.add_resource(HelloWorld,'/')
api.add_resource(RequestApi, '/api/v1/request/<int:id>', endpoint = 'requestapi')
api.add_resource(RequestService, '/api/v1/request', endpoint = 'requestservice')
api.add_resource(UserRegister, '/api/v1/users', endpoint = 'userregister')
api.add_resource(UserRegister, '/api/v1/users/<string:email>', endpoint = 'userregister')
api.add_resource(UserLogin, '/api/v1/users/login', endpoint= 'userlogin')

