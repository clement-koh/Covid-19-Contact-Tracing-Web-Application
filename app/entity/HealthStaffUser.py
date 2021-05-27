from ..dbConfig import dbConnect, dbDisconnect
from .User import User

class HealthStaffUser(User):
	# Constructor
	def __init__(self, NRIC = None):
		# Calls superclass constructor
		super().__init__(NRIC)
		
		# Connect to database
		connection = dbConnect()
		db = connection.cursor()

		# If the id is provided, fill the object with details from database
		hasResult = False
		if id is not None:
			# Select details from database and populate instance variables
			result = db.execute("""SELECT id, NRIC, licenseNo
								   FROM health_staff_user
								   WHERE NRIC = (?)""", (NRIC,)).fetchone()
			
			# Populate private instance variables with value or None 
			if result is not None:
				hasResult = True
				self.__healthStaffUserID = result[0]
				self.__NRIC = result[1]
				self.__licenseNo = result[2]
		
		# If no result
		if not hasResult:
				self.__healthStaffUserID = None
				self.__NRIC = None
				self.__licenseNo = None
		
		# Disconnect from database
		dbDisconnect(connection)

	# Accessor Method
	def getHealthStaffUserID(self):
		return self.__healthStaffUserID

	def getNRIC(self):
		return self.__NRIC

	def getLicenseNo(self):
		return self.__licenseNo
	
	# Other Method
	def hasLicenseRecord(self, licenseNo):
		"""
		Returns True if license already exists
		"""
		# Connect to database
		connection = dbConnect()
		db = connection.cursor()

		# Perform query
		result = db.execute("""SELECT id, NRIC, licenseNo
								   FROM health_staff_user
								   WHERE licenseNo = (?)""", (licenseNo,)).fetchone()
		
		# Disconnect from database
		dbDisconnect(connection)

		return True if result is not None else False
	
	def addNewUser(self, NRIC, firstName, middleName, lastName, gender, 
					mobile, password, licenseNo, accountType='Health Staff'):
		super().addNewUser(NRIC, firstName, middleName, lastName, gender, 
							mobile, password, accountType=accountType)

		# Open connection to database
		connection = dbConnect()
		db = connection.cursor()
		
		# insert new health staff user record
		db.execute("""INSERT INTO health_staff_user(
							NRIC, licenseNo
						)
						VALUES((?), (?))""",
						(NRIC, licenseNo))
		
		# Commit the update to the database
		connection.commit()

		# Close the connection to the database
		dbDisconnect(connection)

		# Check if any rows have been updated successfully
		if db.rowcount != 0:
			print("Added Health User")
			return True
		
		# If no rows has been updated
		return False

	def updateExistingUser(self, firstName, middleName, lastName,
							gender, mobile, password, licenseNo):
		# Call the parent method
		super().updateExistingUser(firstName, middleName, lastName,
									gender, mobile, password)
		
		# Open connection to database
		connection = dbConnect()
		db = connection.cursor()
		
		# Update the health staff user record
		db.execute("""UPDATE health_staff_user
						SET licenseNo = (?)
						WHERE NRIC = (?)""", (licenseNo, self.__NRIC))
		
		# Commit the update to the database
		connection.commit()

		# Close the connection to the database
		dbDisconnect(connection)

		# Check if any row has been updated successfully
		if db.rowcount != 0:
			print("Updated Health Staff User")
			return True
		
		# If no row has been updated
		return False