import datetime

from app import db
from app.auth.models import User


class Categories(db.Model):
    '''Class to represent category table for events'''
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    def __repr__(self):
        '''Returns readable representation of the object'''
        return "Category: {}" .format(self.name)

    def save(self):
        '''save created category to the database'''
        db.session.add(self)
        db.session.commit()

    def delete(self):
        '''delete existing category from the database'''
        db.session.delete(self)
        db.session.commit()


class Events(db.Model):
    '''Class to represent events table'''

    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(Categories.id), nullable=False)
    name = db.Column(db.String(100), unique=True, index=True)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, default=0)
    location = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)
    dueDate = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    maxNumOfAttendees = db.Column(db.Integer, nullable=False)
    isPublic = db.Column(db.Boolean, default=True)
    dateCreated = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    dateModified = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    category = db.relationship("Categories", backref=db.backref("Events", 
                               cascade="all, delete-orphan"))

    def __repr__(self):
        '''Returns readable representation of the object'''
        return "User: {}" .format(self.name)

    def save(self):
        '''save created event to the database'''
        db.session.add(self)
        db.session.commit()

    def delete(self):
        '''delete existing event from the database'''
        db.session.delete(self)
        db.session.commit()
