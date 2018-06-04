from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask_restful import abort
from flask_restful import reqparse


class UserDao(object):

    def __init__(self, id,email, username, password, user_type):
        self.user_id = id
        self.email = email
        self.username = username
        self.password = password
        self.user_type = user_type


users = []
users.append(UserDao(id=1,email='alovegakevin@gmail.com', username='alovega', password='kev1234', user_type='user'))
users.append(UserDao(id=2,email='amanda@hotmail.com', username='amandachoxxs', password='amanda4567', user_type='Admin'))

resource_fields = {
    'email': fields.String,
    'username': fields.String,
    'password': fields.String,
    'user_type': fields.String
}
reqparse = reqparse.RequestParser()
reqparse.add_argument('email', type=str, required=True, help='No user email provided', location='json')
reqparse.add_argument('username', type=str, required=True, help='please choose username', location='json')
reqparse.add_argument('password', type=str, required=True, help='include password', location='json')

class Userregister(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = reqparse.parse_args()
        new_id = len(users)
        user = UserDao(
            user_id=new_id,
            email=args['email'],
            username=args['username'],
            password=args['password'],
            user_type=args['user']
        )
        users.append(user)
        return user, 201

    @marshal_with(resource_fields)
    def get(self, id):
        for user in users:
            if (user.user_id == id):
                return user
        abort(404)

    @marshal_with(resource_fields)
    def put(self, id):
        for user in users:
            if (user.id == id):
                args = reqparse.parse_args()
                user.email = args['email']
                user.username = args['username']
                user.password = args['password']
                return user

        abort(404)
