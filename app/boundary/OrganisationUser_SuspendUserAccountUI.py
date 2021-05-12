from flask import flash, redirect, session, render_template
from ..controllers.OrganisationUser_SuspendUserAccountController import OrganisationUser_SuspendUserAccountController
from flask import session, url_for


class OrganisationUser_SuspendUserAccountUI:
	# Empty Constructor
	def __init__(self):
		pass

	def onSubmit(self, NRIC):
		"""
		Updates Account Status to suspend or not.
		Returns True if the Account status is updated successfully.
		"""
		# Ensure the user is authorised to perform this functionality
		userType = session['userType']
		if userType != "Organisation":
			flash("Unauthorised access to this content", "error")
			return redirect("/")

		# Set session to record the user viewed
		session['viewingNRIC'] = NRIC
		
		# Create controller to update SuspendAccount Status
		controller = OrganisationUser_SuspendUserAccountController()

		# Calls the controller to update SuspendAccount status
		result = controller.updateAccountStatus(NRIC)
		
		# Returns True if successfully updated / False if failed to update
		return result

	def displayError(self):
		"""
		Displays the Account status of Users
		with an error message
		"""

		# Error message to be displayed
		message = "Failed to Change Account Status"

		# Flask error message
		flash(message, 'error')

		#redirect to ViewUserAccount route
		return redirect(url_for('.ViewUserAccount'))
		

	def displaySuccess(self):
		"""
		Display message to inform the User account status had successful change
		"""

		# store successful message
		message = "Account suspension status has been updated successfully"

		# Flash Successful message
		flash(message, 'message')

		#redirect to ViewUserAccount route
		return redirect(url_for('.ViewUserAccount'))