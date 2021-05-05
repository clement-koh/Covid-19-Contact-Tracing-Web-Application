from flask import flash, redirect, session, render_template
from ..controllers.HealthStaffUser_UpdateVaccinationController import HealthStaffUser_UpdateVaccinationController


class HealthStaffUser_UpdateVaccinationUI:
	# Empty Constructor
	def __init__(self):
		pass


	def displayPage(self):
		"""
		Displays the update vaccination status page with details of the patient
		"""
        
		# Ensure that the user is authroised to access this page, otherwise redirect to other page
		userType = session['userType'] 
		if userType!= "Health Staff":
			flash("Unauthorised to access this content", 'error')
			return redirect('/')
		
		
		return render_template('healthStaff_viewUpdateVaccination.html', userType=session['userType'])

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

	def displayError(self, message):
		"""
		Displays the update status of patient
		with an error message
		"""

		flash(message, 'error')
		return self.displayPage()
		

	def displaySuccess(self):
		"""
		Displays the update status of patient
		with a message to inform the health stuff that the update was successful
		"""

		flash('Vaccination Status updated', 'message')
		return self.displayPage()