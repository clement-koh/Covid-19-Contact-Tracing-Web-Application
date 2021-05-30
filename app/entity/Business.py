from ..dbConfig import dbConnect, dbDisconnect

class Business:
	# Constructor
	def __init__(self, id = None):
		# Connect to database
		connection = dbConnect()
		db = connection.cursor()

		# If the id is provided, fill the object with details from database
		hasResult = False
		if id is not None:
			# Select location from database and populate instance variables
			result = db.execute("""SELECT id, name
								   FROM business 
								   WHERE id = (?)""", (id,)).fetchone()
			
			# Populate private instance variables with value or None 
			if result is not None:
				hasResult = True
				self.__id = result[0]
				self.__name = result[1]
		
		# If no result
		if not hasResult:
				self.__id = None
				self.__name = None
		
		# Disconnect from database
		dbDisconnect(connection)

	# Accessor Method
	def getID(self):
		return self.__id

	def getName(self):
		return self.__name
	
	# Other Method
	def getAllBusinessID(self):
		"""
		Returns a int array of all businessID
		"""
		# Open connection to database
		connection = dbConnect()
		db = connection.cursor()

		# Select User from database and populate instance variables
		results = db.execute("""SELECT id FROM business""").fetchall()

		# Disconnect from database
		dbDisconnect(connection)

		# Returns a list of all NRIC
		idList = []
		for result in results:
			idList.append(int(result[0]))
		
		return idList

	
	def getAllBusinessName(self):
		"""
		Returns a string array of all businessID
		"""
		# Open connection to database
		connection = dbConnect()
		db = connection.cursor()

		# Select User from database and populate instance variables
		results = db.execute("""SELECT name FROM business""").fetchall()

		# Disconnect from database
		dbDisconnect(connection)

		# Returns a list of all business name
		nameList = []
		for result in results:
			nameList.append(result[0])
		
		return nameList


	def getIDfromName(self, name):
		""" 
		Return None if there is no result, or 
		Return a integer id, returns -1 if no result
		"""
		# Connect to database
		connection = dbConnect()
		db = connection.cursor()

		# Select location name from id
		result = db.execute("""SELECT id
							   FROM business 
							   WHERE name = (?)""", (name,)).fetchone()

		# Disconnect from database
		dbDisconnect(connection)

		# Return None if no result
		if result is None:
			return -1
		
		# Return the name if there is a result
		return result[0]
