from ..dbConfig import dbConnect, dbDisconnect

class Location:
	# Constructor
	def __init__(self, id = None):
		# Connect to database
		connection = dbConnect()
		db = connection.cursor()

		# If the id is provided, fill the object with details from database
		hasResult = False
		if id is not None:
			# Select location from database and populate instance variables
			result = db.execute("""SELECT id, businessID, locationName
								   FROM location 
								   WHERE id = (?)""", (id,)).fetchone()
			
			# Populate private instance variables with value or None 
			if result is not None:
				hasResult = True
				self.__id = result[0]
				self.__businessID = result[1]
				self.__locationName = result[2]
		
		# If no result
		if not hasResult:
				self.__id = None
				self.__businessID = None
				self.__locationName = None
		
		# Disconnect from database
		dbDisconnect(connection)

	# Accessor Method
	def getID(self):
		return self.__id
	
	def getBusinessID(self):
		return self.__businessID

	def getLocationName(self):
		return self.__locationName
	

	# Other Method
	def getLocationNameFromID(self, id):
		""" 
		Return None if there is no result, or 
		Return a string containing the location name
		"""
		# Connect to database
		connection = dbConnect()
		db = connection.cursor()

		# Select location name from id
		result = db.execute("""SELECT locationName
							   FROM location 
							   WHERE id = (?)""", (id,)).fetchone()

		# Disconnect from database
		dbDisconnect(connection)

		# Return None if no result
		if result is None:
			return None
		
		# Return the name if there is a result
		return result[0]

	def getLocationsBelongingToBusiness(self, businessID):
		"""
		Takes in a businessID and 
		returns an int array of locationIDs associated with 
		the businessID
		"""
		# Connect to database
		connection = dbConnect()
		db = connection.cursor()

		# Select all id based on businessID
		result = db.execute("""SELECT id FROM location 
							   WHERE businessID = (?)""", (businessID,)).fetchall()

		# Disconnect from database
		dbDisconnect(connection)

		# Return None if no result
		if result is None:
			return None
		
		# Store all results in a int array
		locationIDs = []
		for item in result:
			locationIDs.append(int(item[0]))
		
		# Return the array of location ID
		return locationIDs
