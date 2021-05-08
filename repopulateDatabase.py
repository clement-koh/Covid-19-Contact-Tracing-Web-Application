### WARNING: ONLY USE THIS IF YOU WANT A CLEAN RESET ON THE DATABASE
###          THIS Will drop all tables and re-create them using a fresh slate
###          ANY CHANGES MADE AFTER INITIAL SETUP WILL BE LOST

# TO REPOPULATE THE DATABASE 
#   1. Copy all classes from entities.py and replace the classes below
#   2. type the following command in command prompt
#      >>> python repopulateDatabase.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from random import randrange, randint, uniform
from datetime import datetime, timedelta

app = Flask(__name__)

# Database Settings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app/db.sqlite3'

db = SQLAlchemy(app)

# -------------------------------------------------
#               Editable Settings
# -------------------------------------------------
# Location History Settings
CHANCE_TO_GO_OUT = 33          # In percentage (33%)
MIN_LOCATION_VISITED = 1        # No of location
MAX_LOCATION_VISITED = 3        # No of location

# Infection Setting
POPULATION_PERCENTAGE_CONFIRMED_INFECTED_DAILY = 0.01	  # In percentage (0.01%)

# Vaccination Settings (Sum to 100)
NOT_ELIGIBLE_FOR_VACCINATION = 10 							
ELIGIBLE_FOR_VACCINATION = 20
SCHEDULED_FOR_FIRST_SHOT = 30
SCHEDULED_FOR_SECOND_SHOT = 40
VACCINATION_COMPLETED = 100 - NOT_ELIGIBLE_FOR_VACCINATION - \
						ELIGIBLE_FOR_VACCINATION - \
						SCHEDULED_FOR_FIRST_SHOT - \
						SCHEDULED_FOR_SECOND_SHOT

# COPIES OF ALL ENTITY BELOW. COPY ALL CLASS ENTITY FROM ENTITIES.PY BEFORE RUNNING CODE
class Business(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(50), unique=True, nullable=False)
	
class Organisation(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(50), unique=True, nullable=False)

class Location(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	businessID = db.Column(db.String(10), db.ForeignKey('business.id'), nullable=False)
	locationName = db.Column(db.String(100), unique=True, nullable=False)

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
	accountType = db.Column(db.String(50), nullable=False)

class BusinessUser(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), unique=True, nullable=False)
	businessID = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)

class HealthStaffUser(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), unique=True, nullable=False)
	licenseNo = db.Column(db.Integer, unique=True, nullable=False)

class OrganisationUser(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), unique=True, nullable=False)
	organisationID = db.Column(db.Integer, db.ForeignKey('organisation.id'), nullable=False)

class Alert(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	sent_by = db.Column(db.String(10), db.ForeignKey('user.NRIC'), nullable=False)
	sent_on = db.Column(db.DateTime, nullable=False, default=datetime.now())
	alert_type = db.Column(db.String(100), nullable=False)
	recipient_NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), nullable=False,)
	message = db.Column(db.Text, nullable=False)
	read_on = db.Column(db.DateTime)
	is_read = db.Column(db.Boolean, default=False)

class LocationHistory(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), nullable=False)
	location_visited = db.Column(db.Integer, db.ForeignKey('location.id'), autoincrement=True)
	time_in = db.Column(db.DateTime, nullable=False)
	time_out = db.Column(db.DateTime, nullable=False)

class InfectedPeople(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), nullable=False)
	infected_on = db.Column(db.DateTime, nullable=False)
		
class VaccinationStatus(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	NRIC = db.Column(db.String(10), db.ForeignKey('user.NRIC'), nullable=False)
	vaccinationStatus = db.Column(db.String(50), nullable=False)
	dateOfFirstShot = db.Column(db.DateTime)
	dateOfSecondShot = db.Column(db.DateTime)
	

# Code to create and populate data

#16 ^ 3  = 4096 unique names / accounts
firstName = ['Addison', 'Bowie', 'Carter', 'Drew', 'Eden', 'Finn', 'Gabriel', 'Hayden', 'Jamie', 'Jules', 'Ripley', 'Skylar', 'Ashton', 'Caelan', 'Flynn', 'Kaden']
middleName = ['Angel', 'Asa', 'Bay', 'Blue', 'Cameron', 'Gray', 'Lee', 'Quinn', 'Rue', 'Tate', 'Banks', 'Quince', 'Finley', 'Shea', 'Pace', 'James']
lastName = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia', 'Wilson', 'Taylor', 'Moore', 'White', 'Anderson', 'Rodriguez', 'Lopez', 'Walker']
gender = ['M', 'F']

businessID = range(1, 11)
businessName = ['Bapple', 'Amazone', 'Fishbook', 'Boogle', 'McRonald\'s', '7-Melon', 'Sunbucks', 'Blokeswagon', 'Cola Coca', 'Borgar King']
branchLocation = ['Ang Mo Kio', 'Bishan', 'Choa Chu Kang', 'Woodlands', 'Punggol', 'Tampines', 'Pasir Ris', 'Yishun', 'Jurong', 'Sengkang']


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
			mobile = 90000000 + count
			random_gender = randint(0,len(gender)-1)

			if count < 1000:
				accountType = 'Public'
			elif 1000 <= count < 2000:
				accountType = 'Health Staff'
			elif 2000 <= count < 3000:
				accountType = 'Business'
			else:
				accountType = 'Organisation'

		
			# Add User
			newUser = User(NRIC=NRIC,
						   password=NRIC,
						   firstName=x, 
						   middleName=y, 
						   lastName=z, 
						   mobile=mobile, 
						   gender=gender[random_gender],
						   accountType=accountType)
			db.session.add(newUser)
			print('User added. {} new users added.'.format(count), end =' ')


			if count < 1000:
				print('Account type: Public')

			# Generate a health user
			elif 1000 <= count < 2000:
				licenseNo += 1
				newHealthStaffUser = HealthStaffUser(NRIC=NRIC, licenseNo=licenseNo)
				db.session.add(newHealthStaffUser)
				print('Account type: Health Staff')

			# Generate a business user
			elif 2000 <= count < 3000:
				random_businessID = randint(1,len(businessID))
				newBusinessUser = BusinessUser(NRIC=NRIC, businessID=random_businessID)
				db.session.add(newBusinessUser)
				print('Account type: Business')

			# Generate a organisation user
			else:
				newOrganisationUser = OrganisationUser(NRIC=NRIC, organisationID=1)
				db.session.add(newOrganisationUser)
				print('Account type: Organisation')


# Generate Locations (100 Locations)
count = 1
allLocations = {}
for business in businessName:
	for branch in branchLocation:
		locationName = '{} - {} Branch'.format(business, branch)
		allLocations[count] = locationName
		newLocation = Location(businessID=count, locationName=locationName)
		db.session.add(newLocation)
		print('Location entity has been created - {}'.format(locationName))
	count += 1



# Variable Setup
totalNumberOfUsers = range(1, 4097)
numOfDays = range(31, -1, -1)
today = datetime.now()
today = today.replace(hour=0, minute=0, second=0, microsecond=0)


# Generate Location History
noOfRecords = 0
for i in numOfDays:
	for userID in totalNumberOfUsers:
		NRIC = 'S'+ '{:04d}'.format(userID)
		# Random chance to visit location
		chance = randint(0, 100)

		# if user goes out
		if chance <= CHANCE_TO_GO_OUT:

			# Randomly generate number of place visited
			numOfLocationVisited = randint(MIN_LOCATION_VISITED, MAX_LOCATION_VISITED)
			locationVisited = []

			# Add all location visited
			for location in range(numOfLocationVisited):
				visitLocation = randint(1, 100)
				while visitLocation in locationVisited:
					visitLocation = randint(1, 100)
				locationVisited.append(visitLocation)

			# Add to location history
			for location in locationVisited:
				time_in = today - timedelta(i)
				time_in_hour = randint(0, 21)
				time_in_min = randint(0, 59)
				time_in = time_in.replace(hour=time_in_hour, minute=time_in_min)
				time_out = time_in.replace(hour=time_in_hour + randint(1, 2), minute=randint(0, 59))

				newLocationRecord = LocationHistory(NRIC=NRIC, location_visited=location, time_in=time_in , time_out=time_out)
				db.session.add(newLocationRecord)
				noOfRecords += 1
				print('Location History Record on {}. Total Location history Record = {}'.format(time_in, noOfRecords))

# Generate Infected Record
noOfRecords = 0
for i in numOfDays:
	for userID in totalNumberOfUsers:            
		NRIC = 'S'+ '{:04d}'.format(userID)
		# Random chance to visit location
		chance = uniform(0.00, 100.00)

		#if user is infected
		if chance <= POPULATION_PERCENTAGE_CONFIRMED_INFECTED_DAILY:
			infected_on = visited_on = today - timedelta(i)
			newinfectedRecord = InfectedPeople(NRIC=NRIC, infected_on=infected_on)
			db.session.add(newinfectedRecord)
			noOfRecords += 1
			print('Infected History Recorded on {}. Total Infected Individual Record = {}'.format(infected_on, noOfRecords))


# Generate random vaccination status
for userID in totalNumberOfUsers:
	NRIC = 'S'+ '{:04d}'.format(userID)
	
	# Chance for a random vaccination Status 
	chance = uniform(0.00, 100.00)
	
	# Set a status for the user
	status = None

	# If not eligible for vaccination 
	if chance <= NOT_ELIGIBLE_FOR_VACCINATION:
		status = "Not Eligible for Vaccination"
	else:
		chance -= NOT_ELIGIBLE_FOR_VACCINATION

	# if Eligible for vaccination
	if status is None and chance <= ELIGIBLE_FOR_VACCINATION:
		status = "Eligible for Vaccination"
	else:
		chance -= ELIGIBLE_FOR_VACCINATION

	# if Scheduled for first shot
	if status is None and chance <= SCHEDULED_FOR_FIRST_SHOT:
		status = "Scheduled for First Shot"
	else:
		chance -= SCHEDULED_FOR_FIRST_SHOT
	
	# if scheduled for second shot
	if status is None and chance <= SCHEDULED_FOR_SECOND_SHOT:
		status = "Scheduled for Second Shot"
	else:
		status = "Vaccination Completed"

	start_date = datetime(2021, 4, 1)
	end_date = datetime.today()

	time_between_dates = end_date - start_date
	days_between_dates = time_between_dates.days
	random_number_of_days = randrange(days_between_dates)
	# get first random date
	random_date = start_date + timedelta(days=random_number_of_days)




	


	

# Commit Records
db.session.commit()
print('All entries committed to database')
