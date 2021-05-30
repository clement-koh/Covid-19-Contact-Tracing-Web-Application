from ..dbConfig import dbConnect, dbDisconnect

class LocationHistory:
	# Constructor
	def __init__(self, id = None):
		# Connect to database
		connection = dbConnect()
		db = connection.cursor()

		# If the id is provided, fill the object with details from database
		hasResult = False
		if id is not None:
			# Select location history from database and populate instance variables
			result = db.execute("""SELECT id, NRIC, location_visited, time_in,
										  time_out
								   FROM location_history 
								   WHERE id = (?)""", (id,)).fetchone()
			
			# Populate private instance variables with value or None 
			if result is not None:
				hasResult = True
				self.__id = result[0]
				self.__NRIC = result[1]
				self.__locationVisited = result[2] 
				self.__time_in = result[3]
				self.__time_out = result[4]
		
		# If no result
		if not hasResult:
				self.__id = None
				self.__NRIC = None
				self.__locationVisited = None 
				self.__time_in = None
				self.__time_out = None
		
		# Disconnect from database
		dbDisconnect(connection)

	# Accessor Method
	def getID(self):
		return self.__id
	
	def getNRIC(self):
		return self.__NRIC
	
	def getTimeIn(self):
		return self.__time_in
	
	def getTimeOut(self):
		return self.__time_out

	# Other Method
	def getPastLocationHistory(self, NRIC, noOfDays):
		""" 
		Return None if there is no result, or 
		Return a 2d array containing all results
		"""
		# Connect to database
		connection = dbConnect()
		db = connection.cursor()

		#Format statement for SQL
		date = "-{} days".format(noOfDays)

		# Select location history within past __ of days based on NRIC
		result = db.execute("""SELECT id, NRIC, location_visited, time_in,
									  time_out
							   FROM location_history 
							   WHERE NRIC = (?) AND
							   		 date(time_in) >= strftime('%Y-%m-%d', date(date('now','localtime')), (?))
							   ORDER BY time_in DESC""", 
							(NRIC, date)).fetchall()

		# Disconnect from database
		dbDisconnect(connection)

		return result

	def getLocationHistoryOn(self, NRIC, noOfDaysAgo):
		""" 
		Return None if there is no result, or 
		Return an array containing all locationID
		"""
		# Connect to database
		connection = dbConnect()
		db = connection.cursor()

		#Format statement for SQL
		date = "-{} days".format(noOfDaysAgo)
		
		latestDate = None
		if noOfDaysAgo > 0:
			latestDate = "-{} days".format(noOfDaysAgo - 1)
		else: 
			latestDate = "+{} days".format(noOfDaysAgo + 1)

		# Select location history within past __ of days based on NRIC
		results = db.execute("""SELECT id, NRIC, location_visited, time_in,
									  time_out
							   FROM location_history 
							   WHERE NRIC = (?) AND
							   		 date(time_in) >= strftime('%Y-%m-%d', date(date('now','localtime')), (?)) AND
									 date(time_in) < strftime('%Y-%m-%d', date(date('now','localtime')), (?))
							   ORDER BY time_in DESC""", 
							(NRIC, date, latestDate)).fetchall()

		# Disconnect from database
		dbDisconnect(connection)

		# Get all infected people's locationID
		locationList = []
		for result in results:
			locationList.append(result[2])

		# Return the list of locationID
		return locationList
	
	def getLocationCheckInDetails(self, locationID, noOfDaysAgo, NRICList):
		""" 
		Return 2d array containing details
		[][0] - id
		[][1] - NRIC
		[][2] - location_visited
		[][3] - time_in
		[][4] - time_out
		"""
		# Connect to database
		connection = dbConnect()
		db = connection.cursor()

		#Format statement for SQL
		date = "-{} days".format(noOfDaysAgo)
		
		latestDate = None
		if noOfDaysAgo > 0:
			latestDate = "-{} days".format(noOfDaysAgo - 1)
		else: 
			latestDate = "+{} days".format(noOfDaysAgo + 1)

		
		query = """SELECT id, NRIC, location_visited, time_in, time_out
					FROM location_history 
					WHERE 
						date(time_in) >= strftime('%Y-%m-%d', date(date('now','localtime')), (?)) AND
						date(time_in) < strftime('%Y-%m-%d', date(date('now','localtime')), (?)) AND
						location_visited = (?) AND 
						NRIC IN ({seq})
					ORDER BY time_in DESC""".format(seq=','.join(['?']*len(NRICList)))

		# Prepare query arguments
		queryArgs = [date, latestDate, locationID]
		for item in NRICList:
			queryArgs.append(item)

		# Select location history within past __ of days based on NRIC
		results = db.execute(query, queryArgs).fetchall()

		# Disconnect from database
		dbDisconnect(connection)

		# Return the list of locationID
		return results