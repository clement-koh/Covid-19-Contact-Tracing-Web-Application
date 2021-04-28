from ..entity.LocationHistory import LocationHistory
from ..entity.InfectedPeople import InfectedPeople

class PublicUser_ExposureStatusController:
	def __init__(self):
		# Public instance variables
		self.DAYS_CONSIDERED_AS_INFECTED = 14
		self.EXPOSURE_RED = 'Red'
		self.EXPOSURE_ORANGE = 'Orange'
		self.EXPOSURE_GREEN = 'Green'

	def getExposureStatus(self, NRIC):
		"""
		Returns 'Red' if the person is an infected individual
		Returns 'Yellow' if the person has been in the same area
		on the same day as an infected person
		Returns 'Green' if none of the other two is met
		"""
		
		# Initialise an Infected People entity object
		infectedPeople = InfectedPeople()

		# If person with NRIC has been infected in the past X days, they will be considered
		# as still infected until the 14 days are up
		if infectedPeople.isInfected(NRIC, self.DAYS_CONSIDERED_AS_INFECTED):
			return self.EXPOSURE_RED

		# Gets an array of infected people
		for daysAgo in range(self.DAYS_CONSIDERED_AS_INFECTED):
			# Get an array of infected people on a specific day
			infected = infectedPeople.getInfectedPeople(daysAgo, self.DAYS_CONSIDERED_AS_INFECTED)

			# Initialise Location History entity
			locationHistory = LocationHistory()

			allInfectedLocation = []
			# Get all infected locations for one of the 14 days
			for people in infected:
				allInfectedLocation += locationHistory.getLocationHistoryOn(people, daysAgo)
		
			# Get all locations visited by the user on one of the 14 days
			visitedLocation = locationHistory.getLocationHistoryOn(NRIC, daysAgo)

			# Check if any user visited any infected location on the same day
			visited = any(item in visitedLocation for item in allInfectedLocation)

			# If he visited any location return yellow exposure
			if visited:
				return self.EXPOSURE_ORANGE
		
		# If none of the location are visited
		return self.EXPOSURE_GREEN