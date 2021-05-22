from ..dbConfig import dbConnect, dbDisconnect
from .User import User


class OrganisationUser(User):
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
			result = db.execute("""SELECT id, NRIC, organisationID
								   FROM organisation_user 
								   WHERE NRIC = (?)""", (NRIC,)).fetchone()
			
			# Populate private instance variables with value or None 
			if result is not None:
				hasResult = True
				self.__organisationUserID = result[0]
				self.__NRIC = result[1]
				self.__organisationID = result[2]
		
		# If no result
		if not hasResult:
				self.__organisationUserID = None
				self.__name = None
				self.__organisationID = None
		
		# Disconnect from database
		dbDisconnect(connection)

	# Accessor Method
	def getOrganisationUserID(self):
		return self.__organisationUserID

	def getNRIC(self):
		return self.__NRIC

	def getOrganisationID(self):
		return self.__organisationID
	

	# Other Method
	def addNewUser(self, NRIC, firstName, middleName, lastName, gender, 
					mobile, password, organisationID, accountType='Organisation'):
		super().addNewUser(NRIC, firstName, middleName, lastName, gender, 
							mobile, password, accountType=accountType)

		# Open connection to database
		connection = dbConnect()
		db = connection.cursor()
		
		# insert new organisation user record
		db.execute("""INSERT INTO organisation_user(
							NRIC, organisationID
						)
						VALUES((?), (?))""",
						(NRIC, organisationID))
		
		# Commit the update to the database
		connection.commit()

		# Close the connection to the database
		dbDisconnect(connection)

		# Check if any rows have been updated successfully
		if db.rowcount != 0:
			print("Added Organisation User")
			return True
		
		# If no rows has been updated
		return False
	
	def updateExistingUser(self, firstName, middleName, lastName,
							gender, mobile, password, organisationID):
		# Call the parent method
		super().updateExistingUser(firstName, middleName, lastName,
									gender, mobile, password)

		# Open connection to database
		connection = dbConnect()
		db = connection.cursor()
		
		# Update the health staff user record
		db.execute("""UPDATE organisation_user
						SET organisationID = (?)
						WHERE NRIC = (?)""", (organisationID, self.__NRIC))
		
		# Commit the update to the database
		connection.commit()

		# Close the connection to the database
		dbDisconnect(connection)

		# Check if any row has been updated successfully
		if db.rowcount != 0:
			print("Updated Organisation User")
			return True
		
		# If no row has been updated
		return False