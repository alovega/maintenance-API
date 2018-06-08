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

#users = []
#usermodels.insert_user(UserDao(  username='alovega', email='alovegakevin@gmail.com', password='kev1234'))
#usermodels.insert_user(UserDao( username='amandachoxxs', email='amanda@hotmail.com', password='amanda4567'))

resource_fields = {
    'email': fields.String,
    'username': fields.String,
    'password': fields.String,
}
reqparse = reqparse.RequestParser()
reqparse.add_argument('username', type=str, required=True, help='please choose username', location='json')
reqparse.add_argument('email', type=str, required=True, help='No user email provided', location='json')
reqparse.add_argument('password', type=str, required=True, help='include password', location='json')

reqparse_copy = reqparse.copy()
reqparse_copy.remove_argument('user_id')
reqparse_copy.remove_argument('email')
reqparse_copy.add_argument('username', type=str, required=True, help='Invalid username', location='json')
reqparse_copy.add_argument('password', type=str, required=True, help='Invalid password', location='json')



class UserRegister(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = reqparse.parse_args()
        user = UserDao(
            username=args['username'],
            email=args['email'],
            password=args['password'],
        )

        maintenanceDao.insert_user(user)
        return user, 201
        print(user)

    @marshal_with(resource_fields)
    def get(self):
        users = maintenanceDao.getAll()
        return users


class UserLogin(Resource):

    @marshal_with(resource_fields)
    def post(self):
        args = reqparse_copy.parse_args ()
        result  = maintenanceDao.get_user_by_email_and_name( args['password'],args['username'])
        if result:
            return  result
        abort(404)

    # @marshal_with(resource_fields)
    # def put(self, id):
    #     for user in usermodels:
    #         if user.user_id == id:
    #             args = reqparse.parse_args()
    #             user.username = args['username']
    #             user.email = args['email']
    #             user.password = args['password']
    #             usermodels.insert_user(user)
    #             return user
