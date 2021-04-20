# from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        message = "{}. {}"
        return message.format(self.id, self.name)

class Organisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        message = "{}. {}"
        return message.format(self.id, self.name)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    NRIC = db.Column(db.String(10), unique=True, nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    middleName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    # date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        message = "{} {} {}"
        return message.format(self.firstName, self.middleName, self.lastName)

class BusinessUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), unique=True, nullable=False)
    businessID = db.Column(db.String(10), db.ForeignKey('business.id'), unique=True, nullable=False)

class HealthStaffUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), unique=True, nullable=False)
    licenseNo = db.Column(db.Integer, unique=True, nullable=False)

class OrganisationUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), unique=True, nullable=False)
    organisationID = db.Column(db.String(10), db.ForeignKey('organisation.id'), unique=True, nullable=False)

