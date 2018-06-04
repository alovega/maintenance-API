from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask_restful import abort
from flask_restful import reqparse


class RequestDao(object):
    """this is my request class it passes the arguments required in request"""
    def __init__(self, request_id, request_title, request_description, request_category):
        self.request_id = request_id
        self.request_title = request_title
        self.request_description = request_description
        self.request_category = request_category

    def __str__(self):
        return self.request_title


requests = []
requests.append(RequestDao(request_id=1, request_title="laptop", request_description="laptop screen Repair",
                           request_category="maintenance"))
requests.append(RequestDao(request_id=2, request_title="window", request_description="window broken",
                           request_category="maintenance"))

resource_fields = {
"""this serves as a function for a marshal app"""
    'request_id': fields.Integer,
    'request_title': fields.String,
    'request_description': fields.String,
    'request_category': fields.String
}

reqparse = reqparse.RequestParser()
"""this function validates the data the user gives the function"""
reqparse.add_argument('title', type=str, required=True, help='No request title provided', location='json')
reqparse.add_argument('description', type=str, required=True, help='No request description provided', location='json')
reqparse.add_argument('category', type=str, required=True, help='Choose category', location='json')


class HelloWorld(Resource):
    """this is a resource class its basically for
    checking whether your link works"""

    def get(self):
        return {'hello': 'world'}


class RequestApi(Resource):
    """this resource class defines updates"""
    @marshal_with(resource_fields)
    def get(self, id):
        for request in requests:
            if (request.request_id == id):
                return request
        abort(404)

    @marshal_with(resource_fields)
    def put(self, id):
        for request in requests:
            if (request.request_id == id):
                args = reqparse.parse_args()
                request.request_title = args['title']
                request.request_description = args['description']
                request.request_category = args['category']
                return request

        abort(404)


class RequestService(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return requests

    @marshal_with(resource_fields)
    def post(self):
        args = reqparse.parse_args()
        request = RequestDao(
            request_id=requests[-1].request_id + 1,
            request_title=args['title'],
            request_description=args['description'],
            request_category=args['category']
        )
        requests.append(request)
        return request, 201
