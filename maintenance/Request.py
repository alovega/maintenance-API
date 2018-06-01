import json

from json import JSONEncoder
from flask_restful import fields, marshal_with, Resource, abort, reqparse


class RequestDao(object):
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
    'request_id': fields.Integer,
    'request_title': fields.String,
    'request_description': fields.String,
    'request_category': fields.String
}


class RequestApi(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        for request in requests:
            if (request.request_id == id):
                return request
        abort(404)


reqparse = reqparse.RequestParser()
reqparse.add_argument('title', type=str, required=True, help='No request title provided', location='json')
reqparse.add_argument('description', type=str, default="", location='json')
reqparse.add_argument('category', type=str, default="", location='json')


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