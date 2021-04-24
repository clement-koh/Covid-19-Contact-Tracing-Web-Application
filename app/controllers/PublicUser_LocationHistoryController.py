from ..entity.LocationHistory import LocationHistory
from ..entity.Location import Location

class PublicUser_LocationHistoryController:
	# Constructor
	def __init__(self):
		""" 
		Construct a object for this current user
		"""
		# Public instance variables
		# Gets all records within the last __ days
		self.HISTORY_NUMBER_OF_DAYS = 14

		# Create private instance variables
		self.__locationHistory = LocationHistory()	# Initialise LocationHistory Object
		self.__location = Location()				# Initialise Location Object


	def getLocationHistory(self, NRIC):
		"""
		Gets a 2D array containing results from the database.
		returns[recordNo][columnNumber].
		Column 0: id, 
		Column 1: NRIC, 
		Column 2: location name, 
		Column 3: time_in, 
		Column 4: time_out, 
		"""
		
		# Returns the result of the query
		return self.__locationHistory.getPastLocationHistory(NRIC, self.HISTORY_NUMBER_OF_DAYS)

	def getLocationName(self, id):
		"""
		Converts the id of a location to the name of a location
		"""
		return self.__location.getLocationNameFromID(id)


