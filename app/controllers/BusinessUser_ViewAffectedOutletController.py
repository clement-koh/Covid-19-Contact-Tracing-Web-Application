from ..entity.BusinessUser import BusinessUser
from ..entity.Location import Location
from ..entity.LocationHistory import LocationHistory
from ..entity.InfectedPeople import InfectedPeople
import json
from datetime import datetime

class BusinessUser_ViewAffectedOutletController:
	def __init__(self):
		self.SHOW_RECORD_NO_OF_DAYS = 14	# No of days to show(exlusive of today)
		self.INFECTION_TIME = 14			# Duration to consider as infected

	def getUserBusinessID(self, NRIC):
		# Create a businessUser entity object
		businessUser = BusinessUser(NRIC)

		# Returns the id of the business the user belongs to
		return businessUser.getBusinessID()

	def getAllBusinessLocation(self, businessID):
		# Create a location entity object
		location = Location()

		return location.getLocationsBelongingToBusiness(businessID)

	def getBusinessInfectedRecord(self, locationIDArray):
		"""
		Returns a JSON string containing the data for each location infected check ins
		date, timeIn and timeOut
		"""

		# InfectedPeople and LocationHistory Entity Objects
		infectedPeople = InfectedPeople()
		locationHistory = LocationHistory()
		location = Location()

		# Create a 2d array to store all infected individuals on each day
		# Generate a record for each daily for SHOW_RECORD_NO_OF_DAYS days
		# (Excluding today)
		# Generates 0-14 days(inclusive) = 15 days of records total
		infectedIndividuals = []
		for daysAgo in range(self.SHOW_RECORD_NO_OF_DAYS + 1):
				infectedIndividuals.append(infectedPeople.getInfectedPeople(daysAgo, self.INFECTION_TIME))

		# For each location
		locationRecord = [] 		# Create a dictionary to store location records
		for locationID in locationIDArray:
			day = 0
			# Get a infected check in record
			infectedCheckIns = {}
			infectedCheckIns['locationName'] = location.getLocationNameFromID(locationID)
			infectedCheckIns['checkInData'] = []

			# Get the check in records for today + past 14 days
			while day <= self.SHOW_RECORD_NO_OF_DAYS:
				# Get the location history of infected people on this day
				history = locationHistory.getLocationCheckInDetails(locationID, day, infectedIndividuals[day])

				# If there are visitations
				if history is not None:
					# Cycle through each item
					for item in history:
						
						# Convert to datetime object
						checkInTime = datetime.strptime(item[3], '%Y-%m-%d %H:%M:%S.%f')
						checkoutTime = datetime.strptime(item[4], '%Y-%m-%d %H:%M:%S.%f')

						# Format the datetime object into a readable string
						checkInRecord = {}
						checkInRecord['date'] = checkInTime.strftime('%d %b %Y')
						checkInRecord['timeIn'] = '{:02d}:{:02d}'.format(checkInTime.hour,
														  				 checkInTime.minute)
						checkInRecord['timeOut'] = '{:02d}:{:02d}'.format(checkoutTime.hour,
														    			  checkoutTime.minute)

						# Adds the record into the checkInData
						infectedCheckIns['checkInData'].append(checkInRecord)
				
				# Increase day count by 1
				day += 1
			# Add the records for one location
			locationRecord.append(infectedCheckIns)
			
		return json.dumps(locationRecord)




			
			





	