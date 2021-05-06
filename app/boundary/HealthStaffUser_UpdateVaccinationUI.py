from flask import flash, redirect, session, render_template
from ..controllers.HealthStaffUser_UpdateVaccinationController import HealthStaffUser_UpdateVaccinationController
from flask import session, url_for

class HealthStaffUser_UpdateVaccinationUI:
	# Empty Constructor
	def __init__(self):
		pass


	def onSubmit(self, NRIC, vaccination_Status, dateOfFirstShot, dateOfSecondShot):
		"""
		Checks if mobile is 8 characters and not empty. Calls relevant function
		for the controller handle the request to update mobile number
		Returns True if mobile number is updated successfully
		"""
        
      
		# Create controller to update vaccination Status
		controller = HealthStaffUser_UpdateVaccinationController()

	

		# Calls the controller to update vaccination status
		result = controller.updateVaccinationStatus(NRIC, vaccination_Status, dateOfFirstShot, dateOfSecondShot)
		
		# Returns True if successfully updated / False if failed to update
		return result

	def displayError(self):
		"""
		Displays the update status of patient
		with an error message
		"""

		messages = "Failed to update vaccination status"

		flash(messages, 'error')

		#redirect to viewUpdateVaccination route
		return redirect(url_for('.viewUpdateVaccination'))
		

	def displaySuccess(self):
		"""
		Displays the update status of patient
		with a message to inform the health stuff that the update was successful
		"""

		#store successful message in session 
		messages = "Vaccination Status updated"

		#Flash Successful message
		flash(messages)

		#redirect to viewUpdateVaccination route
		return redirect(url_for('.viewUpdateVaccination'))