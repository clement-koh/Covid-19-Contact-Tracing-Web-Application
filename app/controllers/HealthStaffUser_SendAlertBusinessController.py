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
		return self.__business.getAllBusinessName()

	def sendAlert(self, businessName, message, sender):
		"""
			Requests the alert entity to send a new alert
			Returns the validation code
			0 - Success
			1 - Business Name not found
			2 - Fail to send to users in the business
		"""

		# Get the business name list
		businessNameList = self.getRecipientList()

		# 1. Check if Business Name Exists
		if not businessName in businessNameList:
			return 1

		# Gets the business ID
		businessID = self.__business.getIDfromName(businessName)

		# Gets the users in the businss
		userList = self.__businessUser.getUsersInBusiness(businessID)

		# Sets the alert type
		alertType = 'Business - {}'.format(businessName)
		count = 0

		# 2. Check if all users in the business receive the alert
		for user in userList:
			if self.__alert.newAlert(sender, alertType, user, message):
				count += 1

		if count != len(userList):
			return 2
			
		# Return Success
		return 0
