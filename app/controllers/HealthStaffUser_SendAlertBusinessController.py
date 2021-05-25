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
		"""
		# Validation code to display specific error message
		validationCode = -1

		# Get the business name list
		businessNameList = self.getRecipientList()

		# Validate if the business name exist
		for name in businessNameList:
			if businessName == name:
				validationCode = 0
		
		# Check if business name exist
		if validationCode == -1:
			return validationCode

		# Gets the business ID
		businessID = self.__business.getIDfromName(businessName)

		# Gets the users in the businss
		userList = self.__businessUser.getUsersInBusiness(businessID)

		# Sets the alert type
		alertType = 'Business - {}'.format(businessName)
		count = 0

		# Check if all users in the business receive the alert
		for user in userList:
			if self.__alert.newAlert(sender, alertType, user, message):
				count += 1

		if count != len(userList):
			print("Number of alerts sent does not match number of users")
			validationCode = -2
			return validationCode
			
		validationCode = 0
		return validationCode

