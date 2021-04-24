from flask import render_template, redirect, session, flash
from ..controllers.User_UpdateContactController import User_UpdateContactController

class User_UpdateContactUI:
	# Empty Constructor
	def __init__(self):
		pass

	def displayPage(self):
		"""
		Displays the update contact page with details of the current user
		"""

		# Create controller to update personal details
		controller = User_UpdateContactController()
		
		NRIC = session['user']
		firstName = controller.getUserFirstName(NRIC)
		middleName = controller.getUserMiddleName(NRIC)
		lastName = controller.getUserLastName(NRIC)
		mobile = controller.getUserMobile(NRIC)
		
		return render_template('general_updateContactDetails.html', userType=session['userType'],
																	firstName=firstName,
																	middleName=middleName,
																	lastName=lastName,
																	NRIC=NRIC,
																	mobile=mobile)


	def onSubmit(self, mobile):
		"""
		Checks if mobile is 8 characters and not empty. Calls relevant function
		for the controller handle the request to update mobile number
		Returns True if mobile number is updated successfully
		"""

		# Create controller to update personal details
		controller = User_UpdateContactController()
		
		# Check if mobile is empty or less than 8 characters
		if mobile is None or len(str(mobile)) != 8:
			return False

		# Calls the controller to update the user's mobile number
		NRIC = session['user']
		result = controller.updateMobile(NRIC, int(mobile))
		
		# Returns True if successfully updated / False if failed to update
		return result

	def displayError(self, message):
		"""
		Displays the update contact page with details of the current user
		with an error message
		"""

		flash(message, 'error')
		return self.displayPage()
		

	def displaySuccess(self):
		"""
		Displays the update contact page with details of the current user
		with a message to inform the user that the update was successful
		"""

		flash('Particulars updated', 'message')
		return self.displayPage()

	
