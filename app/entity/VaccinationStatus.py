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
	