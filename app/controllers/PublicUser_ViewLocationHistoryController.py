from ..entity.LocationHistory import LocationHistory
from ..entity.Location import Location
from datetime import datetime

class PublicUser_ViewLocationHistoryController:
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
		results = self.__locationHistory.getPastLocationHistory(NRIC, self.HISTORY_NUMBER_OF_DAYS)
		
		# Create an empty array
		locationHistory = []

		# Check if result is empty
		if results is not None:
			# Populate the dictionary after formating the results to be display
			for result in results:
				
				checkInTime = datetime.strptime(result[3], '%Y-%m-%d %H:%M:%S')
				checkoutTime = datetime.strptime(result[4], '%Y-%m-%d %H:%M:%S')

				# Create an empty dictionary
				record = {}

				# Records the location name
				record['locationName'] = self.__location.getLocationNameFromID(result[2])
				
				# Gets the date
				record['date'] = checkInTime.strftime('%d %b %Y') 
				
				# Format the time in 24 hours timing (eg. 13:45)
				record['time_in'] = '{:02d}:{:02d}'.format(checkInTime.hour,
														   checkInTime.minute)
				record['time_out'] = '{:02d}:{:02d}'.format(checkoutTime.hour,
														    checkoutTime.minute)

				# Add the dictionary into the array
				locationHistory.append(record)

		return locationHistory