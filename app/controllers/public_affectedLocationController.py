from ..entities import Location, LocationHistory, InfectedPeople
from datetime import datetime, timedelta

class public_affectedLocationController:
	@classmethod
	def getInfectedLocationHistory(cls, no_of_days):
		# Get result from entity
		records = []
		today = datetime.now()
		today = today.replace(hour=0, minute=0, second=0, microsecond=0)
		
		# Cycle through x Number of days
		for i in range(0, no_of_days + 1):
			result = {}
			record_date = today - timedelta(days=i)

			# Save the details in a dictionary
			result['date'] = record_date.strftime('%d %b %Y') 
			result['no_of_cases'] = len(InfectedPeople.getCurrentlyInfected(record_date))
			result['locations'] = sorted(cls._getXDaysAgoInfectedLocation(i))
			
			# Save the dictionary in the list
			records.append(result)
		
		# Return list of all results
		return records

	@staticmethod
	def _getXDaysAgoInfectedLocation(no_of_days):
		# Get todays date
		today = datetime.now()
		today = today.replace(hour=0, minute=0, second=0, microsecond=0)
		
		# Find the date of X days ago
		searchDate = today - timedelta(no_of_days)

		# Find the people infected X days ago
		currentlyInfected = InfectedPeople.getCurrentlyInfected(searchDate)

		# Find all locationsID visited by the infected X days ago
		visitedLocationsID = set()
		for NRIC in currentlyInfected:
			locations = LocationHistory.getLocationHistoryByDate(NRIC, searchDate)
			for locationID in locations:
				visitedLocationsID.add(locationID)
		visitedLocationsID = sorted(visitedLocationsID)

		# Convert all locationID to location Name
		visitedLocationName = set()
		for locationID in visitedLocationsID:
			visitedLocationName.add(Location.getName(locationID))

		return visitedLocationName

	@classmethod
	def getInfectedLocationHistory2(cls, no_of_days):
		# Get result from entity
		today = datetime.now()
		today = today.replace(hour=0, minute=0, second=0, microsecond=0)

		result = {}
		record_date = today - timedelta(days=no_of_days)

		# Save the details in a dictionary
		result['date'] = record_date.strftime('%d %b %Y') 
		result['no_of_cases'] = len(InfectedPeople.getCurrentlyInfected(record_date))
		result['locations'] = sorted(cls._getXDaysAgoInfectedLocation(no_of_days))

		return result