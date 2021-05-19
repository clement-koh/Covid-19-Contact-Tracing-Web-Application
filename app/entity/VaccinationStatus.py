from ..dbConfig import dbConnect, dbDisconnect
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
	def updateVaccinationStatus(self, NRIC, vaccinationStatus, firstShotCheckboxStatus, secondShotCheckboxStatus):
		""" 
		Updates the status of the patient
		Returns True if updated successfully
		Returns False if update failed
		"""

		#change input text for vaccinationStatus
		status = {
			"not_eligible": "Not Eligible for Vaccination",
			"eligible": "Eligible for Vaccination",
			"first_dose_scheduled": "Scheduled for First Shot",
			"second_dose_scheduled": "Scheduled for Second Shot",
			"vaccination_completed": "Vaccination Completed"
		}

		# Get option selected as String representation
		vaccinationStatus = status[vaccinationStatus]

		# current date and time
		now = datetime.now() 

		#format current date and time
		current_dateTime = now.strftime("%m/%d/%Y, %H:%M:%S")

		# Set dateTime for first shot and second shot
		firstShotDate = None
		secondShotDate = None

		# Get existing date, or set new date if none
		if vaccinationStatus == "Scheduled for Second Shot" or vaccinationStatus == "Vaccination Completed":
			if firstShotCheckboxStatus == "checked" and self.getFirstShotDate() is None:
				firstShotDate = current_dateTime
			else:
				firstShotDate = self.getFirstShotDate()
		
		if vaccinationStatus == "Vaccination Completed":
			if secondShotCheckboxStatus == "checked" and self.getSecondShotDate() is None:
				secondShotDate = current_dateTime
			else:
				secondShotDate = self.getSecondShotDate()

		# Open connection to database
		connection = dbConnect()
		db = connection.cursor()
		
		#if patients have a record
		if(self.__NRIC == NRIC):
			# Update the vaccination status for the patient
			db.execute("""UPDATE vaccination_status
						SET vaccinationStatus = (?), dateOfFirstShot = (?), dateOfSecondShot = (?)
						WHERE NRIC = (?)""", (vaccinationStatus, firstShotDate, secondShotDate, self.__NRIC))
		
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

		# Update the object's variables
		self._NRIC = NRIC
		self.__vaccinationStatus = vaccinationStatus
		self.__firstShotDate = firstShotDate
		self.__secondShotDate = secondShotDate

		# Check if any rows have been updated successfully
		if db.rowcount != 0:
			return True
		
		# If no rows has been updated
		return False
	