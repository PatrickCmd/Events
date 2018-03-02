from flask_jwt_extended import (create_access_token)

from app import jwt


def create_auth_token(user_id, email, first_name, last_name):
    """
    Generates the Auth Token
    :return: string
    """
    user = {
        'id': user_id,
        'email': email,
        'first_name': first_name,
        'last_name': last_name
    }

    token = create_access_token(user, expires_delta=False)
    return token
