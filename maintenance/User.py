from flask_restful import fields
from flask_restful import Resource
from flask_restful import reqparse
from flask_jwt_extended import (create_access_token,create_refresh_token,
                                jwt_required,jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
from passlib.hash import pbkdf2_sha256 as sha256
from models.models import MaintenanceDb
from models.RevokedToken import RevokedTokenModel

maintenanceDao = MaintenanceDb()


class UserDao(object):
    def __init__(self,username,email, password):
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def generate_hash(password):
        return sha256.hash (password)

    @staticmethod
    def verify_hash(password,hash):
        return sha256.verify(password,hash)


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
        username = args['username']

        if not username:
          return {"message":"username not valid"},404

        user = UserDao(
            email=args['email'],
            username=username,
            password=args['password']

        )
        if maintenanceDao.check_user_exist(user.email):
            return {"message": "Email already used"}, 202

        user.password = user.generate_hash(user.password)

        try:
            maintenanceDao.insert_user (user)
            access_token = create_access_token (identity=user.username)
            refresh_token = create_refresh_token (identity=user.username)
            return {
                'message': 'User {} was created'.format (user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            },201
        except:
            return {'message': 'Something went wrong'}, 500

        return{
                'message': 'User {0} was created'.format(user.username)
            }, 201

    def get(self):
        users = maintenanceDao.get_all()
        return users


class UserLogin(Resource):
    def post(self):
        args = reqparse_copy.parse_args()
        user = maintenanceDao.get_user_by_username(args['username'])
        if not user:
             return{'message': 'User{} doesn\'t exist'.format(args['username'])}
        if UserDao.verify_hash(args.password, user[0]['password']):
            access_token = create_access_token (identity=user[0]['username'])
            refresh_token = create_refresh_token (identity=user[0]['username'])
            return {
                'message': 'Logged in as {}'.format (user[0]['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return{
                'message':'wrong credentials provided'
            }, 404

    def update_to_admin(self):
        pass


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:

            revoked_token = RevokedTokenModel()
            revoked_token.add_token(jti)
            return {'message': 'Access token has been revoked'},200
        except:
            return {'message':'something went wrong'},500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel()
            revoked_token.add_token(jti)
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'},500



