from flask import flash, redirect, session, render_template
from ..controllers.OrganisationUser_SuspendUserAccountController import OrganisationUser_SuspendUserAccountController
from flask import session, url_for


class OrganisationUser_SuspendUserAccountUI:
	# Empty Constructor
	def __init__(self):
		pass


	def onSubmit(self, NRIC, AccountStatus):
		"""
		Updates Account Status to suspend or not.
		Returns True if the Account status is updated successfully.
		"""

		# Set session to record the user viewed
		session['viewVaccinationInformation'] = NRIC
		
		# Create controller to update SuspendAccount Status
		controller = OrganisationUser_SuspendUserAccountController()

		# Calls the controller to update SuspendAccount status
		result = controller.updateAccountStatus(NRIC, AccountStatus)
		
		# Returns True if successfully updated / False if failed to update
		return result

	def displayError(self):
		"""
		Displays the Account status of Users
		with an error message
		"""

		message = "Failed to Change Account Status"

		flash(message, 'error')

		#redirect to ViewUserAccount route
		return redirect(url_for('.ViewUserAccount'))
		

	def displaySuccess(self):
		"""
		Display message to inform the User account status had successful change
		"""

		#store successful message in session 
		message = "Account Status Change Successful"

		#Flash Successful message
		flash(message, 'message')

		#redirect to ViewUserAccount route
		return redirect(url_for('.ViewUserAccount'))