from ..entity.InfectedPeople import InfectedPeople
from ..entity.Location import Location
from ..entity.LocationHistory import LocationHistory

class OrganisationUser_GenerateInfectionReportController:
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

	def getInfectionData(self, days_ago):
		""" 
		Returns a string array
		Takes in an input to returns an array of infected people's NRIC ___ days ago

		Takes in an input to return an array of:
		[0]: The number of infected people ___ days ago
		[1]: An array of location names that were visited by infected people
		"""
		infectedPeople = self.__infectedPeople.getInfectedPeople(days_ago,self.INFECTION_TIME)
		
		# Array of location ID
		visitedLocations = []

		# Combine all location for all people
		for person in infectedPeople:
			visitedLocations += self.__locationHistory.getLocationHistoryOn(person, days_ago)

		# Array of location names
		locationNamesTemp = []

		# Combine all location names
		for id in visitedLocations:
			locationNamesTemp.append(self.__location.getLocationNameFromID(id))

		# Sort the location name array
		locationNames = sorted(locationNamesTemp)

		return [len(infectedPeople), locationNames]