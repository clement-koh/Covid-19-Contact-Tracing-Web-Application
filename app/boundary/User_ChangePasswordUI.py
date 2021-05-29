from flask import render_template, redirect, session, flash
from ..controllers.User_ChangePasswordController import User_ChangePasswordController

class User_ChangePasswordUI:
	# Empty Constructor 
	def __init__(self):
		pass
	
	def displayPage(self):
		"""
		Displays the update password page
		"""

		return render_template('general_settings.html', userType=session['userType'])

	def isFieldsEmpty(self, old_pw, new_pw1, new_pw2):
		"""
		Returns True if any fields are empty
		"""

		if not old_pw or not new_pw1 or not new_pw2:
			return True
		return False

	def isMatchingPassword(self, pw1, pw2):
		"""
		Returns true if the passwords entered are the same
		"""

		return pw1 == pw2

	def onSubmit(self, old_pw, new_pw):
		"""
	 	Calls relevant function for the controller handle the 
		request to update password. Returns True if password 
		is updated successfully
		"""

		# Create controller to update personal details
		controller = User_ChangePasswordController()

		# Calls the controller to update the user's password
		NRIC = session['user']
	
		
		# return result(True/False) of attempt to update password
		return controller.updatePassword(NRIC ,old_pw, new_pw)

	def displaySuccess(self):
		"""
		Displays the current page to inform the user of the successful changes
		"""
		
		flash("Password Changed", 'message')
		return self.displayPage()

	def displayError(self, message):
		"""
		Displays the current page with an error message
		"""

		flash(message, 'error')
		return self.displayPage()
