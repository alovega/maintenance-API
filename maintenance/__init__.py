from flask import Flask
from flask_restful import Api

from maintenance.Request import HelloWorld, RequestApi, RequestService
from maintenance.User import Userregister

app = Flask(__name__)
api = Api(app)
api.add_resource(HelloWorld,'/')
api.add_resource(RequestApi, '/api/v1/request/<int:id>', endpoint = 'requestapi')
api.add_resource(RequestService, '/api/v1/request', endpoint = 'requestservice')
api.add_resource(Userregister, '/api/v1/user/<int:id>', endpoint = 'user')

