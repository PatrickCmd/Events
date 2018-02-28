import os
from app.settings import BASE_DIR


class BaseConfig(object):
    TESTING = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Production(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class Development(BaseConfig):
    DEBUG = True


class Testing(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')


app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production
}