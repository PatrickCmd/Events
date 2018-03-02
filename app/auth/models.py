import datetime

from app import db
# from app.db.base import ModelManager


class User(db.Model):
    '''Class to represent user table'''

    GENDER_TYPES = [
        ('female', 'Female'),
        ('male', 'Male')
    ]

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(200))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    image = db.Column(db.LargeBinary, nullable=True)
    location = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    date_of_birth = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    date_modified = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        '''Returns readable representation of the object'''
        return "User: {}" .format(self.email)

    def save(self):
        '''save created user to the database'''
        db.session.add(self)
        db.session.commit()

    def delete(self):
        '''delete existing user from the database'''
        db.session.delete(self)
        db.session.commit()
