### WARNING: ONLY USE THIS IF YOU WANT A CLEAN RESET ON THE DATABASE
###          THIS Will drop all tables and re-create them using a fresh slate
###          ANY CHANGES MADE AFTER INITIAL SETUP WILL BE LOST

# TO REPOPULATE THE DATABASE 
#   1. Copy all classes from entities.py and replace the classes below
#   2. type the following command in command prompt
#      >>> python repopulateDatabase.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from random import randrange, randint
from datetime import datetime

app = Flask(__name__)

# Database Settings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

# COPIES OF ALL ENTITY BELOW. COPY ALL CLASS ENTITY FROM ENTITIES.PY BEFORE RUNNING CODE
class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        message = "{}. {}"
        return message.format(self.id, self.name)

    # Search for a business
    @staticmethod
    def getAllBusiness():
        return Business.query.all()

    # Get business ID from business name
    @staticmethod
    def getID(name):
        result = Business.query.filter_by(name=name).first()

        # Id no result is found
        if result is None:
            return None
        
        # If result is found
        return result.id
    

class Organisation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        message = "{}. {}"
        return message.format(self.id, self.name)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NRIC = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    middleName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    accountActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        message = "{} {} {}"
        return message.format(self.firstName, self.middleName, self.lastName)

    # Verify if the user exists, returns True/False
    @staticmethod
    def verifyUser(NRIC, password):
        # Verify the user by their NRIC and password
        result = User.query.filter_by(NRIC=NRIC,password=password).first()
        # select * from user where TABLE COLUMN = 'NRIC_VALUE' AND TABLE COLUMN = 'password value' limit 1;

        # If no result is found
        if result is None:
            return False

        # If result is found
        return True

    # Check if user exists, returns True/False
    @staticmethod
    def getAccountStatus(NRIC):
        result = User.query.filter_by(NRIC=NRIC).first()
        return result.accountActive

    # Search for a user
    @staticmethod
    def getAllUser():
        return User.query.all()
    
    # Check if a NRIC exist in the database
    @staticmethod
    def hasRecord(NRIC):
        result = User.query.filter_by(NRIC=NRIC).first()

        # If no result is found
        if result is None:
            return False

        # If result is found
        return True


class BusinessUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), unique=True, nullable=False)
    businessID = db.Column(db.String(10), db.ForeignKey('business.id'), nullable=False)

    # Verify if the user exists, returns True/False
    @staticmethod
    def verifyUser(NRIC):
        # Verify the user by their NRIC number
        result = BusinessUser.query.filter_by(NRIC=NRIC).first()

        # If no result is found
        if result is None:
            return False

        # If result is found
        return True
    
    @staticmethod
    def getUsers(businessName):
        userQuery = BusinessUser.query\
                                .join(User, User.NRIC==BusinessUser.NRIC)\
                                .join(Business, Business.id==BusinessUser.businessID)\
                                .filter(User.NRIC==BusinessUser.NRIC)\
                                .filter(BusinessUser.businessID==Business.getID(businessName))\
                                .all()
        return userQuery

    

class HealthStaffUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), unique=True, nullable=False)
    licenseNo = db.Column(db.Integer, unique=True, nullable=False)

    # Verify if the user exists, returns True/False
    @staticmethod
    def verifyUser(NRIC):
        # Verify the user by their NRIC number
        result = HealthStaffUser.query.filter_by(NRIC=NRIC).first()

        # If no result is found
        if result is None:
            return False

        # If result is found
        return True

class OrganisationUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), unique=True, nullable=False)
    organisationID = db.Column(db.Integer, db.ForeignKey('organisation.id'), nullable=False)

    # Verify if the user exists, returns True/False
    @staticmethod
    def verifyUser(NRIC):
        # Verify the user by their NRIC number
        result = OrganisationUser.query.filter_by(NRIC=NRIC).first()

        # If no result is found
        if result is None:
            return False

        # If result is found
        return True

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sent_by = db.Column(db.String(10), db.ForeignKey('user.NRIC'), nullable=False)
    sent_on = db.Column(db.DateTime, nullable=False, default=datetime.now())
    alert_type = db.Column(db.String(100), nullable=False)
    recipient_NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), nullable=False,)
    message = db.Column(db.Text, nullable=False)
    read_on = db.Column(db.DateTime)

    @staticmethod
    def addRecord(sent_by, alert_type, recipient_NRIC, 
                  message):
        record = Alert(sent_by=sent_by, alert_type=alert_type,
                       recipient_NRIC=recipient_NRIC,
                       message=message)
        db.session.add(record)
        db.session.commit()
        return record




# Code to create and populate data

#16 ^ 3  = 4096 unique names / accounts
firstName = ['Addison', 'Bowie', 'Carter', 'Drew', 'Eden', 'Finn', 'Gabriel', 'Hayden', 'Jamie', 'Jules', 'Ripley', 'Skylar', 'Ashton', 'Caelan', 'Flynn', 'Kaden']
middleName = ['Angel', 'Asa', 'Bay', 'Blue', 'Cameron', 'Gray', 'Lee', 'Quinn', 'Rue', 'Tate', 'Banks', 'Quince', 'Finley', 'Shea', 'Pace', 'James']
lastName = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia', 'Wilson', 'Taylor', 'Moore', 'White', 'Anderson', 'Rodriguez', 'Lopez', 'Walker']
gender = ['M', 'F']

businessID = range(1, 10)
businessName = ['Bapple', 'Amazone', 'Fishbook', 'Boogle', 'McRonald\'s', '7-Melon', 'Sunbucks', 'Blokeswagon', 'Cola Coca', 'Borgar King']


# Drop all existing tables
db.drop_all()
print('All tables have been dropped')

# Recreate all tables again
db.create_all()
print('All tables have been created')

# Create BUSINESS record
for business in businessName:
    newBusiness = Business(name=business)
    db.session.add(newBusiness)
print('All business entity has been created')

# Create ORGANISATION record
newOrganisation = Organisation(name='Ministry of Health')
db.session.add(newOrganisation)
print('All organisation enity created')

# Create USER record
# All users types are added to this database, before randomly deciding if this user
# is a public, business, health staff, organisation user
count = 0
licenseNo = 10000000

# Generate Users ()
for x in firstName:
    for y in middleName:
        for z in lastName:
            count += 1

            # Generate NRIC
            NRIC = 'S'+ '{:04d}'.format(count)

            # Generate a random usertype
            type = randrange(4)
            mobile = 90000000 + count
            random_gender = randint(0,len(gender)-1)

            # Add User
            newUser = User(NRIC=NRIC,
                           password=NRIC,
                           firstName=x, 
                           middleName=y, 
                           lastName=z, 
                           mobile=mobile, 
                           gender=gender[random_gender])
            db.session.add(newUser)
            print('User added. {} new users added.'.format(count), end =' ')


            if type == 0:
                print('Account type: Public')


            # Generate a business user
            elif type == 1:
                random_businessID = randint(0,len(businessID)-1)
                newBusinessUser = BusinessUser(NRIC=NRIC, businessID=random_businessID)
                db.session.add(newBusinessUser)
                print('Account type: Business')

            # Generate a health user
            elif type == 2:
                licenseNo += 1
                newHealthStaffUser = HealthStaffUser(NRIC=NRIC, licenseNo=licenseNo)
                db.session.add(newHealthStaffUser)
                print('Account type: Health Staff')

            # Generate a organisation user
            else:
                newOrganisationUser = OrganisationUser(NRIC=NRIC, organisationID=1)
                db.session.add(newOrganisationUser)
                print('Account type: Organisation')

# Commit Records
db.session.commit()
print('All entries committed to database')
