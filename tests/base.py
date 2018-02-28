from flask_testing import TestCase

from app import app, db
from app.config import app_config


class BaseTestCase(TestCase):

    def create_app(self):
        config_name = 'testing'
        app.config.from_object(app_config[config_name])
        return app

    def setUp(self):
        app = self.create_app()
        with app.app_context():
            db.create_all()
            db.session.commit()

    def tearDown(self):
        app = self.create_app()
        with app.app_context():
            db.session.remove()
            db.drop_all()