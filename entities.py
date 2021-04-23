from datetime import datetime
from flask import Flask
from .app import db


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

class Location(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	businessID = db.Column(db.String(10), db.ForeignKey('business.id'), nullable=False)
	locationName = db.Column(db.String(100), unique=True, nullable=False)

	# Get all location records
	@staticmethod
	def getAllLocation():
		return Location.query.all()

	# Get location ID from location name
	@staticmethod
	def getID(name):
		result = Location.query.filter_by(locationName=name).first()

		# Id no result is found
		if result is None:
			return None
		
		# If result is found
		return result.id
	
	# Get location ID from location name
	@staticmethod
	def getName(id):
		result = Location.query.filter_by(id=id).first()

		# Id no result is found
		if result is None:
			return None
		
		# If result is found
		return result.locationName


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
        
    #--------------------update personal information and settting-------------------------

    #update personal information
    @staticmethod
    def updateRecord(NRIC, mobile):
       Record = User.query.filter_by(NRIC=NRIC).update(dict(mobile=mobile))
       print(Record)
       db.session.commit()
       return Record

    #get firstname
    @staticmethod
    def getFirstName(NRIC):
        result = User.query.filter_by(NRIC=NRIC).first()
        return result.firstName

    #get lastname
    @staticmethod
    def getLastName(NRIC):
        result = User.query.filter_by(NRIC=NRIC).first()
        return result.lastName

    #get Moblie
    @staticmethod
    def getMobile(NRIC):
        result = User.query.filter_by(NRIC=NRIC).first()
        return result.mobile

    #update password
    @staticmethod
    def updatePassword(NRIC, password):
       Record = User.query.filter_by(NRIC=NRIC).update(dict(password=password))
       print(Record)
       db.session.commit()
       return Record 

    #check passwords
    def checkpasswords(NRIC):
        Record = User.query.filter_by(NRIC=NRIC).first()
        return Record.password

    #--------------------------------end --------------------------------------------



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
	is_read = db.Column(db.Boolean, default=False)

	@staticmethod
	def addRecord(sent_by, alert_type, recipient_NRIC, message):
		record = Alert(sent_by=sent_by, alert_type=alert_type,
					   recipient_NRIC=recipient_NRIC,
					   message=message)
		db.session.add(record)
		db.session.commit()
		return record

	@staticmethod
	def getUserAlert(NRIC):
		result = Alert.query.filter_by(recipient_NRIC=NRIC)\
							.order_by(Alert.sent_on.desc()).all()
		
		if result is not None:
			return result
		else:
			return "no alerts"
	
	@staticmethod
	def updateRecord(id):
		record = Alert.query.filter_by(id=id)\
							.update({Alert.is_read: True,
									Alert.read_on: datetime.now()})
		print(record)
		db.session.commit()
		return record

    
class LocationHistory(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), nullable=False)
	location_visited = db.Column(db.Integer, db.ForeignKey('location.id'), autoincrement=True)
	time_in = db.Column(db.DateTime, nullable=False)
	time_out = db.Column(db.DateTime, nullable=False)

	@staticmethod
	def getLocationHistory(NRIC):
		results = LocationHistory.query\
								.filter_by(NRIC=NRIC)\
								.order_by(LocationHistory.time_in.desc())\
								.all()
		# If no result is found
		if results is None:
			return None

		# If result is found
		return results

	@staticmethod
	def getLocationHistoryByDate(NRIC, date):
		results = LocationHistory.query\
								.filter_by(NRIC=NRIC)\
								.filter(LocationHistory.time_in >= date)\
								.filter(LocationHistory.time_out < (date + timedelta(1)))\
								.order_by(LocationHistory.time_in.desc())\
								.all()
		# If no result is found
		if results is None:
			return None

		# If result is found
		formatted_result = []
		for result in results:
			formatted_result.append(result.location_visited)

		return formatted_result

class InfectedPeople(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), nullable=False)
	infected_on = db.Column(db.DateTime, nullable=False)
	
	@staticmethod
	def getAllRecords():
		earliest_date = datetime.date.today() - datetime.timedelta(days=28)
		result = InfectedPeople.query\
								.filter_by(infected_on > earliest_date)\
								.order_by(infected_on.desc())\
								.all()
		return result

	# Get the NRIC of everyone affect since 14 days before date provided
	@staticmethod
	def getCurrentlyInfected(date):
		earliest_date = date - timedelta(days=14)
		results = InfectedPeople.query\
							   .filter(InfectedPeople.infected_on >= earliest_date)\
							   .filter(InfectedPeople.infected_on < (date + timedelta(1)))\
							   .order_by(InfectedPeople.infected_on.desc())\
							   .all()

		# Return if no results
		if results is None:
			return None

		# Return list of NRIC
		allInfected = []
		for result in results:
			allInfected.append(result.NRIC)
		return allInfected