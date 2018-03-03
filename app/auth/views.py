from flask import request, jsonify, make_response
from flask_restful import Resource
from webargs.flaskparser import use_args
from validate_email import validate_email

from app import bcrypt
from app.auth.models import User
from app.auth.validators import is_valid, name_has_numbers, strip_clean
from app.auth.helpers import create_auth_token
from .args import user_reg_args, login_args


class UserRegistrationView(Resource):
    '''User registration view'''
    @use_args(user_reg_args, locations=('json', 'form'))
    def post(self, args):
        data = request.json
        if name_has_numbers(data):
            response = {
                "messages": "Name field cannot contain numbers"
            }
            return make_response(jsonify(response), 400)
        if is_valid(data['first_name']) or is_valid(data['last_name']):
            response = {
                "messages": "Name contains special characters"
            }
            return make_response(jsonify(response), 400)
        if not validate_email(strip_clean(data['email'])):
            response = {
                "messages": "Invalid email format!"
            }
            return make_response(jsonify(response), 400)
        user = User.query.filter_by(email=strip_clean(data['email'])).first()
        if not user:
            new_user = User(
                email=strip_clean(data['email']),
                password=bcrypt.generate_password_hash(
                    strip_clean(data['password'])).decode('utf-8'),
                first_name=strip_clean(data['first_name']),
                last_name=strip_clean(data['last_name']),
                location=strip_clean(data['location']),
                gender=strip_clean(data['gender'])
            )
            new_user.save()
            user = User.query.filter_by(
                email=strip_clean(data['email'])).first()
            token = create_auth_token(
                user.id,
                strip_clean(data['email']),
                strip_clean(data['first_name']),
                strip_clean(data['last_name'])
            )
            response = {
                "messages": "User account created",
                "token": token
            }
            return make_response(jsonify(response), 201)
        else:
            response = {
                "messages": "User with that email already exists"
            }
            return make_response(jsonify(response), 409)


class UserLoginView(Resource):
    '''User login view'''
    @use_args(login_args, locations=('json', 'form'))
    def post(self, args):
        data = request.json
        if not validate_email(strip_clean(data['email'])):
            response = {
                "messages": "Invalid email format!"
            }
            return make_response(jsonify(response), 400)
        user = User.query.filter_by(
            email=strip_clean(data['email'])).first()
        if user:
            if bcrypt.check_password_hash(user.password,
                                          strip_clean(data['password'])):
                token = create_auth_token(
                    user.id, user.email, user.first_name, user.last_name
                )
                response = {
                    "messages": "Successfully logged in",
                    "token": token
                }
                return make_response(jsonify(response), 200)
            else:
                response = {
                    "messages": "Wrong password, try again!",
                }
                return make_response(jsonify(response), 401)
        else:
            response = {
                    "messages": "User does not exist, please register!",
                }
            return make_response(jsonify(response), 401)
