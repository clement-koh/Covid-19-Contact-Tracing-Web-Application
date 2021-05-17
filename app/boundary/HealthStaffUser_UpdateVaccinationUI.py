from flask import flash, redirect, session, render_template
from ..controllers.HealthStaffUser_UpdateVaccinationController import HealthStaffUser_UpdateVaccinationController
from flask import session, url_for

class HealthStaffUser_UpdateVaccinationUI:
	# Empty Constructor
	def __init__(self):
		pass


	def onSubmit(self, NRIC, vaccination_Status, firstShotCheckboxStatus, secondShotCheckboxStatus):
		"""
		Updates a patient's vaccination status.
		Returns True if the status is updated successfully.
		"""
		
		# Set session to record the user viewed
		session['viewingNRIC'] = NRIC
      
		# Create controller to update vaccination Status
		controller = HealthStaffUser_UpdateVaccinationController()

		# Calls the controller to update vaccination status
		result = controller.updateVaccinationStatus(NRIC, vaccination_Status, firstShotCheckboxStatus, secondShotCheckboxStatus)
		
		# Returns True if successfully updated / False if failed to update
		return result

	def displayError(self):
		"""
		Displays the update status of patient
		with an error message
		"""

		message = "Failed to update vaccination status"

		flash(message, 'error')

		#redirect to viewUpdateVaccination route
		return redirect(url_for('.viewUpdateVaccination'))
		

	def displaySuccess(self):
		"""
		Displays the update status of patient
		with a message to inform the health stuff that the update was successful
		"""

		#store successful message in session 
		message = "Vaccination Status updated"

		#Flash Successful message
		flash(message, 'message')

		#redirect to viewUpdateVaccination route
		return redirect(url_for('.viewUpdateVaccination'))