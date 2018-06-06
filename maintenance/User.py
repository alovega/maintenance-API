from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask_restful import abort
from flask_restful import reqparse


class UserDao(object):

    def __init__(self, user_id, email, username, password):
        self.user_id = user_id
        self.email = email
        self.username = username
        self.password = password


users = []
users.append(UserDao(user_id=1, email='alovegakevin@gmail.com', username='alovega', password='kev1234'))
users.append(UserDao(user_id=2, email='amanda@hotmail.com', username='amandachoxxs', password='amanda4567'))

resource_fields = {
    'user_id': fields.Integer,
    'email': fields.String,
    'username': fields.String,
    'password': fields.String,
}
reqparse = reqparse.RequestParser()
reqparse.add_argument('user_id', type=int, required=True,default="",location='json')
reqparse.add_argument('email', type=str, required=True, help='No user email provided', location='json')
reqparse.add_argument('username', type=str, required=True, help='please choose username', location='json')
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
            user_id= args['user_id'],
            email=args['email'],
            username=args['username'],
            password=args['password'],
        )
        users.append(user)
        return user, 201
        print(user)

    @marshal_with(resource_fields)
    def get(self):
        return users


class UserLogin(Resource):

    @marshal_with(resource_fields)
    def post(self):
        for user in users:
            args = reqparse_copy.parse_args()
            if args['username'] == user.username and args['password'] == user.password:
                return user
        abort(404)

    @marshal_with(resource_fields)
    def put(self, id):
        for user in users:
            if (user.user_id == id):
                args = reqparse.parse_args()
                user.email = args['email']
                user.username = args['username']
                user.password = args['password']
                users.append(user)
                return user
