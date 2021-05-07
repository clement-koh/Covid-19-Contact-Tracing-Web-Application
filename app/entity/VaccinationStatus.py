from ...dbConfig import dbConnect, dbDisconnect
from datetime import datetime


class VaccinationStatus:
	def __init__(self, NRIC=None):
		# Connect to database
		connection = dbConnect()
		db = connection.cursor()

		# If the id is provided, fill the object with details from database
		hasResult = False
		if NRIC is not None:
			# Select from database and populate instance variables
			result = db.execute("""SELECT id, NRIC, vaccinationStatus,
								   dateOfFirstShot, dateOfSecondShot
								   FROM vaccination_status
								   WHERE NRIC = (?)""", (NRIC,)).fetchone()
			
			# Populate private instance variables with value or None 
			if result is not None:
				hasResult = True
				self.__id = result[0]
				self.__NRIC = result[1]
				self.__vaccinationStatus = result[2]
				self.__firstShotDate = result[3]
				self.__secondShotDate = result[4]
		
		# If no result
		if not hasResult:
			self.__id = None
			self.__NRIC = None
			self.__vaccinationStatus = None
			self.__firstShotDate = None
			self.__secondShotDate = None
		
		# Disconnect from database
		dbDisconnect(connection)

	# Accessor Methods
	def getID(self):
		return self.__id
	
	def getNRIC(self):
		return self.__NRIC

	def getVaccinationStatus(self):
		return self.__vaccinationStatus
	
	def getFirstShotDate(self):
		return self.__firstShotDate

	def getSecondShotDate(self):
		return self.__secondShotDate

	# Other Methods


	def updateVaccinationStatus(self, NRIC, vaccinationStatus, firstShotDate, secondShotDate):
		""" 
		Updates the status of the patient
		Returns True if updated successfully
		Returns False if update failed
		"""


		# current date and time
		now = datetime.now() 

		#format datevaccinationStatus
		date = now.strftime("%m/%d/%Y, %H:%M:%S")

		#change input text for vaccinationStatus
		status = {
		"not_eligible": "Not Eligible for Vaccination",
		"eligible": "Eligible for Vaccination",
		"first_dose_scheduled": "Scheduled for First Shot",
		"second_dose_scheduled": "Scheduled for Second Shot",
		"vaccination_completed": "Vaccination Completed"
		}
		vaccinationStatus = status[vaccinationStatus]


		#check status is Scheduled for First Shot 
		if vaccinationStatus == "Scheduled for First Shot":
			firstShotDate = "Not Vaccinated"
			secondShotDate = "Not Vaccinated"

		#check status is Eligible for Vaccination
		if vaccinationStatus == "Eligible for Vaccination":
			firstShotDate = "Not Vaccinated"
			secondShotDate = "Not Vaccinated"

		#check status is Not Eligible for Vaccination
		if vaccinationStatus == "Not Eligible for Vaccination":
			firstShotDate = "Not Vaccinated"
			secondShotDate = "Not Vaccinated"

		#check status is Scheduled for Second Shot
		if vaccinationStatus == "Scheduled for Second Shot":
			firstShotDate = date
			secondShotDate = "Not Vaccinated"

		#check status is Vaccination Completed
		if vaccinationStatus == "Vaccination Completed":
			firstShotDate = self.__firstShotDate
			secondShotDate = date


		
		# Update the object's recorded NRIC"
		self._NRIC = NRIC

		# Update the object's recorded vaccination_Status"
		self.__vaccinationStatus = vaccinationStatus

		# Update the object's recorded firstShotDate"
		self.__firstShotDate = firstShotDate


		# Update the object's recorded dateOfSecondShot"
		self.__secondShotDate = secondShotDate

		# Open connection to database
		connection = dbConnect()
		db = connection.cursor()
		

		#if patients have a record
		if(self.__NRIC == NRIC):
			# Update the vaccination status for the patient
			db.execute("""UPDATE vaccination_status
						SET vaccinationStatus = (?), dateOfFirstShot = (?), dateOfSecondShot = (?)
						WHERE NRIC = (?)""", (vaccinationStatus,firstShotDate,secondShotDate, self.__NRIC))
		
		#if patient dont not have a record
		else:
			# insert new vaccination status for the patient
			db.execute("""INSERT INTO vaccination_status(NRIC, vaccinationStatus, dateOfFirstShot, dateOfSecondShot)
						  VALUES((?), (?), (?), (?))""",
						  (NRIC, vaccinationStatus, firstShotDate, secondShotDate))

		# Commit the update to the database
		connection.commit()

		# Close the connection to the database
		dbDisconnect(connection)
		
		# Check if any rows have been updated successfully
		if db.rowcount != 0:
			return True
		
		# If no rows has been updated
		return False
	