"""
Auth application
"""

from flask import Blueprint
from flask_restful import Api
from app.auth.views import UserRegistrationView, UserLoginView

auth = Blueprint('auth', __name__, url_prefix='/auth')
auth_api = Api(auth)

auth_api.add_resource(UserRegistrationView, '/register')
auth_api.add_resource(UserLoginView, '/login')
