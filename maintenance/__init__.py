from flask import Flask
from flask_restful import Api
from maintenance.Request import HelloWorld, RequestUser, RequestPosting, RequestDisapprove, RequestApprove
from  maintenance.Request import RequestUserId
from maintenance.User import UserRegister
from maintenance.User import UserLogin
from flask_jwt_extended import JWTManager
from models import RevokedToken
from maintenance.User import UserLogoutAccess,UserLogoutRefresh
from maintenance.refresh import TokenRefresh
from maintenance.Request import RequestAdmin
from maintenance.Request import RequestAdminId
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']
jwt = JWTManager(app)
api = Api(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedToken.RevokedTokenModel.is_jti_blacklisted(jti)


"""my api resources """
api.add_resource(HelloWorld,'/')
api.add_resource(RequestUser, '/users/requests/<int:user_id>', endpoint='requestapi')
api.add_resource(RequestPosting, '/users/requests', endpoint='requestservice')
api.add_resource(UserRegister, '/auth/signup', endpoint='userregister')
api.add_resource(UserLogin, '/auth/login', endpoint='userlogin')
api.add_resource(RequestUserId,'/users/request/<id>', endpoint='requestuserid')
api.add_resource(UserLogoutRefresh,'/auth/logout/refresh',endpoint='userlogoutrefresh')
api.add_resource(UserLogoutAccess,'/auth/logout', endpoint='userlogout access')
api.add_resource(TokenRefresh,'/token/refresh', endpoint='tokenrefresh')
api.add_resource(RequestAdmin,'/requests/',endpoint='requestadmin')
api.add_resource(RequestAdminId,'/request/<int:id>/resolve',endpoint='requestadminid')
api.add_resource(RequestApprove,'/request/<int:id>/approve',endpoint='requestapprove')
api.add_resource(RequestDisapprove,'/request/<int:id>/disapprove',endpoint='requestdisapprove')