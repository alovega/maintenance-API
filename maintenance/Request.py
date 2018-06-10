from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask_restful import abort
from flask_restful import reqparse
from models.models import MaintenanceDb

maintenanceDao = MaintenanceDb()

class RequestDao(object):
    def __init__(self,author, title, description,category):
        self.author = author
        self.title = title
        self.description = description
        self.category = category

    def __str__(self):
        return self.request_title


requests = []
maintenanceDao.insert_request(RequestDao(author = "kevin",title="laptop",description="laptop screen Repair",category="maintenance"))
requests.append(RequestDao(author = "alovega",title="window", description="window broken",category="maintenance"))

resource_fields = {
    'request_id': fields.Integer,
    'request_title': fields.String,
    'request_description': fields.String,
    'request_category': fields.String
}

reqparse = reqparse.RequestParser()
reqparse.add_argument('title', type=str, required=True, help='No request title provided', location='json')
reqparse.add_argument('description', type=str, required=True, help='No request description provided', location='json')
reqparse.add_argument('category', type=str, required=True, help='Choose category', location='json')


class HelloWorld(Resource):

    def get(self):
        return {'hello': 'world'}


class RequestApi(Resource):
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
