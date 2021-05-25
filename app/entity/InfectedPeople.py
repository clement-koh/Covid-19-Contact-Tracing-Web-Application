from ..dbConfig import dbConnect, dbDisconnect

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
		earliestDate = "-{} days".format(noOfDaysAgo + infection_time)


		# Select location history within past __ of days based on NRIC
		results = db.execute("""SELECT DISTINCT NRIC
							   FROM infected_people
							   WHERE date(infected_on) >= strftime('%Y-%m-%d', date(date('now','localtime')), (?)) AND
							   		 date(infected_on) <= strftime('%Y-%m-%d', date(date('now','localtime')), (?))""", 
							(earliestDate, latestdate)).fetchall()

		# Disconnect from database
		dbDisconnect(connection)

		# Array to hold all NRIC
		NRIClist = []
		
		# Get all infected people's NRIC
		for result in results:
			NRIClist.append(result[0])

		return NRIClist

	def isInfected(self, NRIC, daysConsideredAsInfected):
		""" 
		Return False if there is no result, or 
		Return true if NRIC is infected existing since __ days ago
		"""
		# Connect to database
		connection = dbConnect()
		db = connection.cursor()

		#Format statement for SQL
		latestdate = "+{} days".format(1)
		# 14 days excluding today
		earliestDate = "-{} days".format(daysConsideredAsInfected)

		# Select location history within past __ of days based on NRIC
		results = db.execute("""SELECT count(*)
								FROM infected_people
							   	WHERE NRIC = (?) AND
							   		  date(infected_on) >= strftime('%Y-%m-%d', date(date('now','localtime')), (?)) AND
							   		  date(infected_on) <= strftime('%Y-%m-%d', date(date('now','localtime')), (?))""", 
							(NRIC, earliestDate, latestdate)).fetchone()

		# Disconnect from database
		dbDisconnect(connection)

		# If not infected, return false
		if results[0] == 0:
			return False

		# If infected return True
		return True
	
	def getLastInfectedDate(self, NRIC):
		"""
			Returns the date as a string
			Returns None if no date is found
		"""
		# Connect to database
		connection = dbConnect()
		db = connection.cursor()

		# Select location history within past __ of days based on NRIC
		results = db.execute("""SELECT infected_on
								FROM infected_people
							   	WHERE NRIC = (?)
								ORDER BY infected_on DESC""", 
							(NRIC, )).fetchone()

		# Disconnect from database
		dbDisconnect(connection)

		# If no data is retreieved
		if results is None:
			return results
		
		# Return the retrieved date
		return results[0]