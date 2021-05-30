from flask import session, flash, redirect, render_template
from ..controllers.HealthStaffUser_ViewVaccineStatusController import HealthStaffUser_ViewVaccineStatusController

class HealthStaffUser_ViewVaccineStatusUI:
	# Constructor
	def __init__(self):
		# Define responses status for the class
		self.RESPONSE_SUCCESS = "Success"
		self.RESPONSE_FAILURE_EMPTY_FIELD = "NRIC field cannot be empty"
		self.RESPONSE_FAILURE_INVALID_NRIC = "Invalid NRIC"

		# Private instance variable
		self.__patientNRIC = None 														# Patient's NRIC Number
		self.__viewVaccineStatusController = HealthStaffUser_ViewVaccineStatusController()	# Controller Object

	# Other Method
	def displayPage(self):
		"""
		Displays the page view a Vaccination Status details
		"""
		# Ensure that the user is authroised to access this page, otherwise redirect to other page
		userType = session['userType'] 
		if userType!= "Health Staff":
			flash("Unauthorised to access this content", 'error')
			return redirect('/')

		# If directed here with a user already provided
		if session['viewingNRIC'] is not None:
			# Get provided user details
			self.__patientNRIC = session['viewingNRIC']

			# Remove user details stored
			session['viewingNRIC'] = None

			# Display information of user
			return self.displaySuccess()

		# Render the page
		return render_template('healthStaff_viewUpdateVaccination.html', userType=userType)
	

	def onSubmit(self, NRIC):
		"""
		Firstly, verify the input field is empty, then check if NRIC exists
		Return a response based on the outcome of each check.
		"""
		self.__patientNRIC = NRIC

		# Check if NRIC field is empty
		if self.__patientNRIC is None or len(self.__patientNRIC) == 0:
			return self.RESPONSE_FAILURE_EMPTY_FIELD
		
		# Check if NRIC exists
		if not self.__viewVaccineStatusController.verifyPatient(self.__patientNRIC):
			return self.RESPONSE_FAILURE_INVALID_NRIC
		
		# If all checks successful
		return self.RESPONSE_SUCCESS
	
	def displaySuccess(self):
		"""
		Displays a success page showing the patient's details
		"""
		# Gets the current user type
		userType = session['userType']

		# Get the patient's details
		vaccineStatusDetails = self.__viewVaccineStatusController.getPatientVaccineStatusDetails(self.__patientNRIC)

		# Render the page with patient's details
		return render_template('healthStaff_viewUpdateVaccination.html', userType=userType,
																   vaccineStatusDetails=vaccineStatusDetails)

	def displayError(self, response):
		flash(response, 'error')
		return self.displayPage()