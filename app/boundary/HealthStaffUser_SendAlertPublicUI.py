from flask import flash, redirect, session, render_template
from ..controllers.HealthStaffUser_SendAlertPublicController import HealthStaffUser_SendAlertPublicController

class HealthStaffUser_SendAlertPublicUI:
	# Constructor
	def __init__(self):
		# Public Instance Variable 
		# Responses
		self.RESPONSE_FAILURE_FIELD_EMPTY = "Fields cannot be empty"
		self.RESPONSE_FAILURE_INVALID_RECIPIENT = "Recipient('{}') is not a valid user"
		self.RESPONSE_FAILURE_UNKNOWN_ERROR = "Error sending alert to recipient"
		self.RESPONSE_SUCCESS = "Alert successfully sent to '{}'"

	def displayPage(self):
		"""
		Displays the webpage to send alerts to public user
		"""
		# Ensure that the user is authroised to access this page, otherwise redirect to other page
		userType = session['userType']
		if userType != 'Health Staff':
			flash('You do not have permission to access the requested functionality','error')
			return redirect('/')

		# Display the webpage
		return render_template('healthStaff_new_public_alert.html', userType=userType)

	def onSubmit(self, NRIC, message):
		"""
		Check if NRIC and message fields are blank. Then check if the NRIC is not valid user
		Returns a failure response if either is met. Else return a success response
		"""
		# Initialize Controller Object
		controller = HealthStaffUser_SendAlertPublicController()
		
		# Check if input values are empty
		if NRIC is None or len(NRIC) == 0 or message is None or len(message) == 0:
			return self.RESPONSE_FAILURE_FIELD_EMPTY
		
		# Attempt to send alert
		validationCode = controller.sendAlert(NRIC, message, session['user'])

		# Check if recipient exists
		if validationCode == 1:
			# Update failure response message
			self.RESPONSE_FAILURE_INVALID_RECIPIENT = self.RESPONSE_FAILURE_INVALID_RECIPIENT.format(NRIC)
			return self.RESPONSE_FAILURE_INVALID_RECIPIENT
		
		# If sending of alert met with an error
		elif validationCode == 2:
			# If fail to send, return failure response
			return self.RESPONSE_FAILURE_UNKNOWN_ERROR
			
		# If successful, send the alert
		else:
			# Update the success message
			self.RESPONSE_SUCCESS = self.RESPONSE_SUCCESS.format(NRIC)
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



		