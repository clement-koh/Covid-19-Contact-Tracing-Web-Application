from ..entity.Location import Location
from ..entity.LocationHistory import LocationHistory
from ..entity.InfectedPeople import InfectedPeople

class PublicUser_ViewAffectedLocationController:
	# Constructor
	def __init__(self):
		""" 
		Construct objects for this current user
		"""
		# Public instance variables
		# Gets all records within the last __ days
		self.QUARANTINE_PERIOD = 14

		# Create private instance variables
		self.__location = Location()				# Initialise Location Object
		self.__locationHistory = LocationHistory()	# Initialise LocationHistory Object
		self.__infectedPeople = InfectedPeople()	# Initialise InfectedPeople Object

	def getInfectedPeople(self, days_ago):
		""" 
		Takes in an input to returns an array of infected people's NRIC ___ days ago
		"""
		return self.__infectedPeople.getInfectedPeople(days_ago,self.QUARANTINE_PERIOD)

	def getVisitedLocation(self, days_ago, people):
		""" 
		Takes in a array of NRIC and 
		returns an array of unique locationID visited by everyone in the array
		"""
		allLocation = []

		# Combine all location for all peoplle
		for user in people:
			allLocation += self.__locationHistory.getLocationHistoryOn(user, days_ago)

		# Return an array of unique location ID
		return list(set(allLocation))

	def getLocationName(self, idArray):
		""" 
		Takes in a array of location id and 
		returns an array of location name
		"""
		allLocation = []

		# Combine all location names
		for id in idArray:
			allLocation.append(self.__location.getLocationNameFromID(id))

		# Return an array of unique location name
		return sorted(list(set(allLocation)))
