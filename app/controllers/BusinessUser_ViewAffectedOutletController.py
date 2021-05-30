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

	def getBusinessInfectedRecord(self, NRIC):
		"""
		Returns a 2D string array containing the data for each location infected check ins
		date, timeIn and timeOut

		[x][] - Location Name
		[][0] - Date
		[][1] - Check In Time
		[][2] - Check Out Time
		"""
		# BusinessUser, Location, InfectedPeople and LocationHistory Entity Objects
		businessUser = BusinessUser(NRIC)
		location = Location()
		infectedPeople = InfectedPeople()
		locationHistory = LocationHistory()

		# Returns the id of the business the user belongs to
		businessID = businessUser.getBusinessID()

		# Returns the list of locationsID
		locationIDArray = location.getLocationsBelongingToBusiness(businessID)

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
			infectedCheckIns = []
			infectedCheckIns.append(location.getLocationNameFromID(locationID))
			infectedCheckIns.append([])

			# Get the check in records for today + past 14 days
			while day <= self.SHOW_RECORD_NO_OF_DAYS:
				# Get the location history of infected people on this day
				history = locationHistory.getLocationCheckInDetails(locationID, day, infectedIndividuals[day])

				# If there are visitations
				if history is not None:
					# Cycle through each item
					for item in history:
						
						# Convert to datetime object
						checkInTime = datetime.strptime(item[3], '%Y-%m-%d %H:%M:%S')
						checkoutTime = datetime.strptime(item[4], '%Y-%m-%d %H:%M:%S')

						# Format the datetime object into a readable string
						checkInRecord = []
						checkInRecord.append(checkInTime.strftime('%d %b %Y'))
						checkInRecord.append('{:02d}:{:02d}'.format(checkInTime.hour,
														  				 checkInTime.minute))
						checkInRecord.append('{:02d}:{:02d}'.format(checkoutTime.hour,
														    			  checkoutTime.minute))

						# Adds the record into the checkInData
						infectedCheckIns[1].append(checkInRecord)
				
				# Increase day count by 1
				day += 1
			# Add the records for one location
			locationRecord.append(infectedCheckIns)
			
		return locationRecord




			
			





	