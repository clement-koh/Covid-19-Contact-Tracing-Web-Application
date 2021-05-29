from flask import flash, redirect, session, render_template
from ..controllers.HealthStaffUser_SendAlertBusinessController import HealthStaffUser_SendAlertBusinessController

class HealthStaffUser_SendAlertBusinessUI:
	# Constructor
	def __init__(self):
		# Public Instance Variable 
		# Responses
		self.RESPONSE_FAILURE_FIELD_EMPTY = "Fields cannot be empty"
		self.RESPONSE_FAILURE_INVALID_RECIPIENT = "Recipient('{}') is not a valid user"
		self.RESPONSE_FAILURE_UNKNOWN_ERROR = "Error sending alert to recipient"
		self.RESPONSE_SUCCESS = """Your alert message has been successfully 
                              		delivered to all users in {}!"""

		# Private Instance Variable
		self.__controller = HealthStaffUser_SendAlertBusinessController()	# Initialize Controller Object

	def displayPage(self):
		"""
		Displays the webpage to send alerts to Business user
		"""
		# Ensure that the user is authroised to access this page, otherwise redirect to other page
		userType = session['userType']
		if userType != 'Health Staff':
			flash('You do not have permission to access the requested functionality','error')
			return redirect('/')

		# Get businessName list
		businessNames = self.__controller.getRecipientList()

		# Display the webpage
		return render_template('healthStaff_new_business_alert.html', userType=userType,
														     		  userDetails=businessNames)

	def onSubmit(self, businessName, message):
		"""
		Check if businessName and message fields are blank. 
		Then check if the Business is not valid
		Returns a failure response if either is met.
		Else return a success response
		"""

		# Check if input values are empty
		if businessName is None or len(businessName) == 0 or message is None or len(message) == 0:
			return self.RESPONSE_FAILURE_FIELD_EMPTY

		validationCode = self.__controller.sendAlert(businessName, message, session['user'])
		
		# Check if recipient exists
		if validationCode == 1:
			# Update failure response message
			return self.RESPONSE_FAILURE_INVALID_RECIPIENT.format(businessName)

		# If not all the users in the business receive the alert
		elif validationCode == 2:
			# If fail to send, return failure response
			return self.RESPONSE_FAILURE_UNKNOWN_ERROR

		# If successful
		else:
			# Update the success message
			self.RESPONSE_SUCCESS = self.RESPONSE_SUCCESS.format(businessName)
			return self.RESPONSE_SUCCESS

	def displayError(self, errorMessage):
		"""
		Displays the alert page with a error notification
		"""
		flash(errorMessage, 'error')
		return self.displayPage()

	def displaySuccess(self):
		"""
		Displays the alert page with a success notification
		"""
		flash(self.RESPONSE_SUCCESS, 'message')
		return self.displayPage()



		