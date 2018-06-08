from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask_restful import abort
from flask_restful import reqparse
from models.models import MaintenanceDb


maintenanceDao = MaintenanceDb()


class UserDao(object):

    def __init__(self,username,email, password):
        self.username = username
        self.email = email
        self.password = password


user_fields = {
    'email': fields.String,
    'username': fields.String,
    'password': fields.String,
}


reqparse = reqparse.RequestParser()
reqparse.add_argument('username', type=str, required=True, help='please choose username', location='json')
reqparse.add_argument('email', type=str, required=True, help='No user email provided', location='json')
reqparse.add_argument('password', type=str, required=True, help='include password', location='json')

reqparse_copy = reqparse.copy()
reqparse_copy.remove_argument('email')
reqparse_copy.add_argument('username', type=str, required=True, help='Invalid username', location='json')
reqparse_copy.add_argument('password', type=str, required=True, help='Invalid password', location='json')


class UserRegister(Resource):
    def post(self):
        args = reqparse.parse_args()
        user = UserDao(
            email=args['email'],
            username=args['username'],
            password=args['password'],
        )
        if  maintenanceDao.check_user_exist(user.email):
            return {"message": "Email already used"}, 202
        else:
            maintenanceDao.insert_user(user)
            return user, 201

    @marshal_with(user_fields)
    def get(self):
        users = maintenanceDao.getAll()
        return users


class UserLogin(Resource):
    @marshal_with(user_fields)
    def post(self):
        args = reqparse_copy.parse_args ()
        result = maintenanceDao.get_user_by_password_and_name(args['username'],args['password'])
        if result:
            return result
        abort(404)


class UserUpdate(Resource):
    def put(self, id):
        args = reqparse_copy.parse_args()
        result = maintenanceDao.update_user(args['username'],args['password'])
        if result:
            return result
        abort(404)
