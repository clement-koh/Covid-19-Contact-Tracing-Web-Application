from ..entity.User import User
from ..entity.InfectedPeople import InfectedPeople
import itertools


class HealthStaffUser_ContactTracingController:
	def __init__(self):
		pass

	# get infected people NRIC for the past 14 days
	def getInfectedPeopleNRIC(self, date):

		# Creates a InfectedPeople object
		listNRIC = InfectedPeople.getInfectedPeopleNRIC(self, date)

		# return list of nric according to date of infection
		return listNRIC
    

	def getPatientDetails(self, NRIC):
		""" 
		Returns a string array containing the following information.

		[0] - NRIC, 
		[1] - First Name, 
		[2] - Middle Name, 
		[3] - Last Name, 
		[4] - Mobile Number,
		[5] - Gender
		[6] - Infected On
		
		"""

		#Separate NRIC and infected date
		NRIClist = [item[0] for item in NRIC]
		InfectedDate = [item[1] for item in NRIC]

		#list to store patient detail
		userInfo = []

		#loop through NRIC LIST record
		for i in range(len(NRIClist)):

			# Creates a user object	
			user = User.getUserDetail(self, NRIClist[i])

			#convert string to tuple
			InfectedDateTuple = (InfectedDate[i],)
	
			# store each users detail tuple with infected date tuple to a list 
			userInfo.append(user + InfectedDateTuple)
		
		#return users detail list
		return userInfo

			
	