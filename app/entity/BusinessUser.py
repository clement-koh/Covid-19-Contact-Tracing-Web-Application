from ..dbConfig import dbConnect, dbDisconnect
from .User import User

class BusinessUser(User):
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
			# Select location from database and populate instance variables
			result = db.execute("""SELECT id, NRIC, businessID
								   FROM business_user 
								   WHERE NRIC = (?)""", (NRIC,)).fetchone()
			
			# Populate private instance variables with value or None 
			if result is not None:
				hasResult = True
				self.__businesUserID = result[0]
				self.__NRIC = result[1]
				self.__businessID = result[2]
		
		# If no result
		if not hasResult:
				self.__businessUserID = None
				self.__name = None
				self.__businessID = None
		
		# Disconnect from database
		dbDisconnect(connection)

	# Accessor Method
	def getBusinessUserID(self):
		return self.__businessUserID

	def getNRIC(self):
		return self.__NRIC

	def getBusinessID(self):
		return self.__businessID
	

	# Other Method
	def getUsersInBusiness(self, businessID):
		"""
		Returns a string array of all user's NRIC
		"""
		# Open connection to database
		connection = dbConnect()
		db = connection.cursor()

		# Select User from database and populate instance variables
		results = db.execute("""SELECT NRIC FROM business_user
								WHERE businessID = (?)""", (str(businessID), )).fetchall()

		# Disconnect from database
		dbDisconnect(connection)

		# Returns a list of all NRIC
		NRICList = []
		for result in results:
			NRICList.append(result[0])
		
		return NRICList
	
	def addNewUser(self, NRIC, firstName, middleName, lastName, gender, 
				   mobile, password, businessID, accountType='Business'):
		# call parents method
		super().addNewUser(NRIC, firstName, middleName, lastName, gender, 
							mobile, password, accountType=accountType)
		
		# Open connection to database
		connection = dbConnect()
		db = connection.cursor()
		
		# insert new business user record
		db.execute("""INSERT INTO business_user(
							NRIC, businessID
						)
						VALUES((?), (?))""",
						(NRIC, businessID))
		
		# Commit the update to the database
		connection.commit()

		# Close the connection to the database
		dbDisconnect(connection)

		# Check if any rows have been updated successfully
		if db.rowcount != 0:
			print("Added new Business User")
			return True
		
		# If no rows has been updated
		return False

	def updateExistingUser(self, firstName, middleName, lastName,
							gender, mobile, password, businessID):
		# Call the parent method
		super().updateExistingUser(firstName, middleName, lastName,
									gender, mobile, password)
		
		# Open connection to database
		connection = dbConnect()
		db = connection.cursor()
		
		# Update the business user record
		db.execute("""UPDATE business_user
						SET businessID = (?)
						WHERE NRIC = (?)""", (businessID, self.__NRIC))
		
		# Commit the update to the database
		connection.commit()

		# Close the connection to the database
		dbDisconnect(connection)

		# Check if any row has been updated successfully
		if db.rowcount != 0:
			print("Updated Business User")
			return True
		
		# If no row has been updated
		return False