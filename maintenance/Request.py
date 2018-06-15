import json

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask_restful import abort
from flask_restful import reqparse
from models.models import MaintenanceDb


maintenanceDao = MaintenanceDb()


class RequestDao(object):
    def __init__(self,username, title, description,category):
        self.username = username
        self.title = title
        self.description = description
        self.category = category

    def __str__(self):
        return self.title


resource_fields = {
    'username':fields.String,
    'title': fields.String,
    'description': fields.String,
    'category': fields.String
}

reqparse = reqparse.RequestParser()
reqparse.add_argument('title', type=str, required=True, help='No request title provided', location='json')
reqparse.add_argument('description', type=str, required=True, help='No request description provided', location='json')
reqparse.add_argument('category', type=str, required=True, help='Choose category', location='json')
reqparse_copy = reqparse.copy()
reqparse_copy.add_argument('title', type=str, required=False, location='json')
reqparse_copy.add_argument('description', type=str, required=False, location='json')
reqparse_copy.add_argument('category', type=str, required=False, help='choose category', location='json')


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class RequestUser(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        result = maintenanceDao.get_request_by_username(current_user)
        if result:
            return result
        else:
            return {"message": "not a registered user"}, 404


class RequestId(Resource):
    @jwt_required
    def get(self, id):
        current_user = get_jwt_identity()
        result = maintenanceDao.get_request_by_request_id_and_username(current_user, id)
        if result:
            return result
        else:
            return {"message": "request id not available"}, 404


    @jwt_required
    def put(self, id):
        args = reqparse_copy.parse_args()
        result = maintenanceDao.update_request(args['title'],args['description'],args['category'],id)
        if result == -1:
            return {"message": "unable to edit this request"}, 400
        if result:
            return maintenanceDao.get_request_by_request_id(id)
        else:
            abort (404)


class RequestPosting(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        args = reqparse.parse_args()
        request = RequestDao(
            username=current_user,
            title=args['title'],
            description=args['description'],
            category=args['category']
        )
        return maintenanceDao.insert_request(request),201


class RequestAdmin(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity ()
        user = maintenanceDao.get_user_by_username (current_user)
        # check if user is admin
        if user[0]['is_admin']:
            result = maintenanceDao.getall_requests()
            if result:
                return result
        else:
            return {"message":"not allowed access for current user"},401


class RequestAdminId(Resource):
    @jwt_required
    def put(self,id):
        current_user = get_jwt_identity ()
        user = maintenanceDao.get_user_by_username (current_user)
        # check if user is admin
        if user[0]['is_admin']:
            result = maintenanceDao.admin_resolve_request(id)
            if result:
                return maintenanceDao.get_request_by_request_id(id)
            else:
                return {'message':'request id given not existing'},400
        else:
            return {'message': 'User not Authorized'},401


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
                return {'message':'request id given not existing'},400
        else:
            return {'message': 'User not authorized'},401

class RequestDisapprove(Resource):
    @jwt_required

    def put(self,id):
        current_user = get_jwt_identity ()
        user = maintenanceDao.get_user_by_username (current_user)
        #checkif user is Admin

        if user[0]['is_admin']:
            result = maintenanceDao.admin_disapprove_request(id)
            if result:
                return maintenanceDao.get_request_by_request_id(id)
            else:
                return {'message':'request id given not existing'},400
        else:
            return {'message':'user not authorized'},401