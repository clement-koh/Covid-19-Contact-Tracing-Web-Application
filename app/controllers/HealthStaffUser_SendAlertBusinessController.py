from ..entity.Business import Business
from ..entity.BusinessUser import BusinessUser
from ..entity.Alert import Alert

class HealthStaffUser_SendAlertBusinessController:
	# Empty Constructor
	def __init__(self):
		# Create Private instance variables
		self.__business = Business() 			# Business Entity
		self.__businessUser = BusinessUser()	# BusinessUser Entity
		self.__alert = Alert()					# Alert Entity

	def getRecipientList(self):
		"""
			Returns a string array of all business name
		"""
		# Return array containing all business name
		businessIDArray = self.__business.getAllBusinessID()
		businessNames = []
		for id in businessIDArray:
			businessTemp = Business(id)
			businessNames.append(businessTemp.getName())

		return businessNames

	def verifyBusinessName(self, name):
		"""
			Returns True if the business name provided is valid
		"""
		if self.__business.getIDfromName(name) == -1:
			return False
		return True

	def sendAlert(self, businessName, message, sender):
		"""
			Requests the alert entity to send a new alert
			Returns the number of recipient of that the alert is sent to
		"""

		# Gets the business ID
		businessID = self.__business.getIDfromName(businessName)

		# Gets the users in the businss
		userList = self.__businessUser.getUsersInBusiness(businessID)

		# Sets the alert type
		alertType = 'Business - {}'.format(businessName)
		count = 0
		
		# Sends alert to all users in the business
		for user in userList:
			if self.__alert.newAlert(sender, alertType, user, message):
				count += 1

		if count != len(userList):
			print("Number of alerts sent does not match number of users")
			count = -1
			
		# Returns the number of recipient of that the alert is sent to
		return count

