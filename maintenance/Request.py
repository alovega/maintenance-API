import json

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask_restful import abort
from flask_restful import reqparse
from models.models import MaintenanceDb


maintenanceDao = MaintenanceDb()


class RequestDao(object):
    def __init__(self,user_id, title, description,category):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.category = category

    def __str__(self):
        return self.title


resource_fields = {
    'user_id':fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'category': fields.String
}

reqparse = reqparse.RequestParser()
reqparse.add_argument('user_id', type=int, required=True, help='please provide user_id', location='json')
reqparse.add_argument('title', type=str, required=True, help='No request title provided', location='json')
reqparse.add_argument('description', type=str, required=True, help='No request description provided', location='json')
reqparse.add_argument('category', type=str, required=True, help='Choose category', location='json')
reqparse_copy = reqparse.copy()
reqparse_copy.remove_argument('user_id')
reqparse_copy.add_argument('title', type=str, required=False, location='json')
reqparse_copy.add_argument('description', type=str, required=False, location='json')
reqparse_copy.add_argument('category', type=str, required=False, help='choose category', location='json')


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class RequestUser(Resource):
    @marshal_with(resource_fields)
    @jwt_required
    def get(self, user_id):
        result = maintenanceDao.get_request_by_user_id(user_id)
        if result:
            return result
        else:
            return {"message": "not a registered user"}, 404


class RequestUserId(Resource):
    @marshal_with (resource_fields)
    @jwt_required
    def get(self, id):
        result = maintenanceDao.get_request_by_request_id(id)
        if result:
            return result
        else:
            return {"message": "request id not available"}, 404


    @jwt_required
    def put(self, id):
        args = reqparse_copy.parse_args()
        result = maintenanceDao.update_request(args['title'],args['description'],args['category'],id)
        if result == -1:
            return {"message": "unable to edit this request"}, 201
        if result:
            return maintenanceDao.get_request_by_request_id(id)
        else:
            abort (404)


class RequestPosting(Resource):
    @jwt_required
    @marshal_with (resource_fields)
    def post(self):
        args = reqparse.parse_args()
        request = RequestDao(
            user_id=args['user_id'],
            title=args['title'],
            description=args['description'],
            category=args['category']
        )
        maintenanceDao.insert_request(request)
        return request, 201


class RequestAdmin(Resource):
    @jwt_required
    def get(self):
        result = maintenanceDao.getall_requests()
        if result:
            return result
        else:
            abort(404)


class RequestAdminId(Resource):
    @jwt_required
    def put(self,id):
        result = maintenanceDao.admin_resolve_request(id)
        if result:
            return maintenanceDao.get_request_by_request_id(id)
        else:
            return {'message':'request id given not existing'}


class RequestApprove(Resource):
    @jwt_required
    def put(self,id):
        current_user = get_jwt_identity()
        user = maintenanceDao.get_user_by_username(current_user)
      # check if user is admin
        if user[0]['is_admin']:
            result = maintenanceDao.admin_approve_request(id)

            if result:
                return maintenanceDao.get_request_by_request_id(id)
        else:
            return {'message':'request id given not existing'}


class RequestDisapprove(Resource):
    @jwt_required

    def put(self,id):
        result = maintenanceDao.admin_disapprove_request(id)
        if result:
            return maintenanceDao.get_request_by_request_id(id)
        else:
            return {'message':'request id given not existing'}
