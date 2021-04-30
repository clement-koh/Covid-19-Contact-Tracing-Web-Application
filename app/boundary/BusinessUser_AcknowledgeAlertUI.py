from flask import flash, redirect, request
from ..controllers.BusinessUser_AcknowledgeAlertController import BusinessUser_AcknowledgeAlertController

class BusinessUser_AcknowledgeAlertUI:
	# Constructor
	def __init__(self):
		self.RESPONSE_SUCCESS = "SUCCESS"
		self.RESPONSE_FAILURE = "FAILURE"

	def onSubmit(self, alertID):
		"""
		Return a response depending if the alert status is successfully updated
		"""

		# Create Controller object
		controller = BusinessUser_AcknowledgeAlertController()

		# If successfully mark as read
		if controller.markAlertAsRead(alertID):
			return self.RESPONSE_SUCCESS

		# If unsuccessful
		return self.RESPONSE_FAILURE

	def displaySuccess(self):
		"""
		Displays the alert page with a success notification
		"""
		# Display a success message
		flash('Alert successfully mark as read', 'message')
		
		# Refresh the current page with a notification message
		return redirect(request.url)

	def displayError(self):
		"""
		Displays the alert page with a failure notification
		"""
		# Display a success message
		flash('Unable to mark alert as read', 'errorMessage')
		
		# Refresh the current page with a notification message
		return redirect(request.url)