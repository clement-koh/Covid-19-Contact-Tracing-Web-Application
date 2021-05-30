from ..entity.User import User
from ..entity.InfectedPeople import InfectedPeople
import datetime
from operator import itemgetter


class HealthStaffUser_GenerateContactTracingReportController:
	def __init__(self):
		self.INFECTION_TIME = 14 	# Considered as infected for _ days

	# Get the details of infected people for the past 14 days
	def getInfectedPeopleDetails(self, date):
		""" 
		Returns a 2D string array containing the following information.

		[x][0] - NRIC
		[x][1] - First Name
		[x][2] - Middle Name
		[x][3] - Last Name
		[x][4] - Mobile Number
		[x][5] - Gender
		[x][6] - Infected On
		"""
		# Creates a InfectedPeople object
		infectedPeople = InfectedPeople()

		currentTime = datetime.datetime.today()
		enteredDate = datetime.datetime.strptime(date, '%Y-%m-%d')

		daysAgo = (currentTime - enteredDate).days

		# Gets the NRIC list of infected individuals
		tempNRICList = infectedPeople.getInfectedPeople(daysAgo,self.INFECTION_TIME)

		# return list of unique NRIC
		NRICList = list(set(tempNRICList))
	
		result = []

		for NRIC in NRICList:

			# List to store patient detail
			userInfo = []

			# Get user information
			tempUser = User(NRIC)

			# Get user last infection date
			infectedOnString = infectedPeople.getLastInfectedDate(NRIC)
			infectedOnDateTime = datetime.datetime.strptime(infectedOnString, '%Y-%m-%d %H:%M:%S')
			infectedOnFormatted = infectedOnDateTime.strftime("%d/%m/%Y")

			# Get user details
			userDetails = tempUser.getFullUserData(NRIC)

			# Append data to array
			userInfo.append(NRIC)
			userInfo.append(userDetails[2])
			userInfo.append(userDetails[3])
			userInfo.append(userDetails[4])
			userInfo.append(userDetails[6])
			userInfo.append(userDetails[5])
			userInfo.append(infectedOnFormatted)

			result.append(userInfo)

		# Sorting
		result.sort(key=itemgetter(0))					# sort by NRIC ascending
		result.sort(key=itemgetter(6), reverse=True)	# sort by Date descending
		
		#return users detail list
		return result