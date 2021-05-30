from ..entity.Location import Location
from ..entity.LocationHistory import LocationHistory
from ..entity.InfectedPeople import InfectedPeople
from datetime import datetime, timedelta

class PublicUser_ViewAffectedLocationController:
	# Constructor
	def __init__(self):
		""" 
		Construct objects for this current user
		"""
		# Public instance variables
		# Gets all records within the last __ days
		self.QUARANTINE_PERIOD = 14

	def getAffectedLocationRecords(self, days_ago):
		""" 
		Returns an array containing the following location
		[0] - Date
		[1] - No of cases for the day
		[2] - Affected locations

		""" 
		location = Location()
		locationHistory = LocationHistory()
		infectedPeople = InfectedPeople()

		allLocationID = []
		allLocationName = []

		infectedPeopleArray = infectedPeople.getInfectedPeople(days_ago,self.QUARANTINE_PERIOD)

		# Combine all location ID for all peoplle
		for user in infectedPeopleArray:
			allLocationID += locationHistory.getLocationHistoryOn(user, days_ago)

		# Remove duplicates in the array
		allLocationID = list(set(allLocationID))

		# Combine all location names
		for id in allLocationID:
			allLocationName.append(location.getLocationNameFromID(id))

		# Get the date and time X days ago
		today = datetime.now()
		today = today.replace(hour=0, minute=0, second=0, microsecond=0)
		record_date = today - timedelta(days=days_ago)

		# Format the data to be returned
		result = []
		result.append(record_date.strftime('%d %b %Y'))
		result.append(len(infectedPeopleArray))
		result.append(allLocationName)

		# Return an array of unique location name
		return result