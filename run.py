from flask import Flask
from flask_restful import Api
from maintenance.Request import RequestService, RequestApi,HelloWorld

app = Flask(__name__)
api = Api(app)
api.add_resource(HelloWorld,'/')
api.add_resource(RequestApi, '/api/v1/request/<int:id>', endpoint = 'requestapi')
api.add_resource(RequestService, '/api/v1/request', endpoint = 'requestservice')

if __name__ == '__main__':
    app.run(debug=True)