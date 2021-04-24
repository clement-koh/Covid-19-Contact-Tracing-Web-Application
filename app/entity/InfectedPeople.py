from ...dbConfig import dbConnect, dbDisconnect

class InfectedPeople:
	def __init__(self, id=None):
		# Connect to database
		connection = dbConnect()
		db = connection.cursor()

		# If the id is provided, fill the object with details from database
		hasResult = False
		if id is not None:
			# Select from database and populate instance variables
			result = db.execute("""SELECT id, NRIC, infected_on
								   FROM infected_people
								   WHERE id = (?)""", (id,)).fetchone()
			
			# Populate private instance variables with value or None 
			if result is not None:
				hasResult = True
				self.__id = result[0]
				self.__NRIC = result[1]
				self.__infected_on = result[2]
		
		# If no result
		if not hasResult:
				self.__id = None
				self.__NRIC = None
				self.__infected_on = None
		
		# Disconnect from database
		dbDisconnect(connection)

	# Accessor Method
	def getID(self):
		return self.__id

	def getNRIC(self):
		return self.__NRIC

	def getInfectedOn(self):
		return self.__infected_on

	# Other Method
	def getInfectedPeople(self, noOfDaysAgo, infection_time):
		""" 
		Return None if there is no result, or 
		Return an array containing all NRIC infected existing on __ days ago
		"""
		# Connect to database
		connection = dbConnect()
		db = connection.cursor()

		#Format statement for SQL
		latestdate = "-{} days".format(noOfDaysAgo)
		earliestDate = "-{} days".format(noOfDaysAgo + infection_time + 1)

		# Select location history within past __ of days based on NRIC
		results = db.execute("""SELECT id, NRIC, infected_on
							   FROM infected_people
							   WHERE date(infected_on) >= strftime('%Y-%m-%d', date(date('now','localtime')), (?)) AND
							   		 date(infected_on) < strftime('%Y-%m-%d', date(date('now','localtime')), (?))""", 
							(earliestDate, latestdate)).fetchall()

		# Disconnect from database
		dbDisconnect(connection)

		# Array to hold all NRIC
		NRIClist = []
		
		# Get all infected people's NRIC
		for result in results:
			NRIClist.append(result[1])

		# Return the list of NRIC
		return NRIClist



	