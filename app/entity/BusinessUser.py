from ...dbConfig import dbConnect, dbDisconnect
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
				self.__id = result[0]
				self.__NRIC = result[1]
				self.__businessID = result[2]
		
		# If no result
		if not hasResult:
				self.__id = None
				self.__name = None
				self.__businessID = None
		
		# Disconnect from database
		dbDisconnect(connection)

	# Accessor Method
	def getID(self):
		return self.__id

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
	
	
