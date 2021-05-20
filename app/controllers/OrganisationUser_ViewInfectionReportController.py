from ..entity.InfectedPeople import InfectedPeople
from ..entity.Location import Location
from ..entity.LocationHistory import LocationHistory

class OrganisationUser_ViewInfectionReportController:
	# Empty Constructor
	def __init__(self):
		self.INFECTION_TIME = 14  #No of days to be considered as infected

		# Create private instance variables
		self.__location = Location()				# Initialise Location Object
		self.__locationHistory = LocationHistory()	# Initialise LocationHistory Object
		self.__infectedPeople = InfectedPeople()	# Initialise InfectedPeople Object
	
	# -------------------------------------------------
	#					Infection Chart
	# -------------------------------------------------
	def get2WeekInfectionCount(self):
		"""
		Returns the daily infection count for the past 2 weeks in an array
		Latest date being [13]
		"""
		
		# Create entity object	
		infectedPeople = InfectedPeople()

		# Create an array to store the result
		result = []

		# Gets the number of infected people the last 14 days (include today)
		for i in reversed(range(14)):
			result.append(len(infectedPeople.getInfectedPeople(i, self.INFECTION_TIME)))

		return result
		

	# -------------------------------------------------
	#				Affected Location Detail
	# -------------------------------------------------

	def getInfectedPeople(self, days_ago):
		""" 
		Returns a string array
		Takes in an input to returns an array of infected people's NRIC ___ days ago
		"""
		return self.__infectedPeople.getInfectedPeople(days_ago,self.INFECTION_TIME)

	def getVisitedLocation(self, days_ago, people):
		""" 
		Takes in a array of NRIC and 
		returns an array of int containing locationID visited by everyone in the array
		"""
		allLocation = []

		# Combine all location for all peoplle
		for user in people:
			allLocation += self.__locationHistory.getLocationHistoryOn(user, days_ago)

		# Return an array of location ID
		return allLocation

	def getLocationName(self, idArray):
		""" 
		Takes in a array of location id and 
		returns an string array of location name
		"""
		allLocation = []

		# Combine all location names
		for id in idArray:
			allLocation.append(self.__location.getLocationNameFromID(id))

		# Return an array of location name
		return sorted(allLocation)

