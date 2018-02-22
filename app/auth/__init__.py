"""
Auth application
"""

from flask import Blueprint
from flask_restful import Api

auth = Blueprint('auth', __name__, url_prefix='/auth')
auth_api = Api(auth)
