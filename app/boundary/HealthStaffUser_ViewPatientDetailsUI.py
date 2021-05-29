from flask import session, flash, redirect, render_template
from ..controllers.HealthStaffUser_ViewPatientDetailsController import HealthStaffUser_ViewPatientDetailsController

class HealthStaffUser_ViewPatientDetailsUI:
	# Constructor
	def __init__(self):
		# Define responses status for the class
		self.RESPONSE_SUCCESS = "Success"
		self.RESPONSE_FAILURE_EMPTY_FIELD = "NRIC field cannot be empty"
		self.RESPONSE_FAILURE_INVALID_NRIC = "Invalid NRIC"

		# Private instance variable
		self.__patientNRIC = None 														# Patient's NRIC Number
		self.__viewPatientController = HealthStaffUser_ViewPatientDetailsController()	# Controller Object

	# Other Method
	def displayPage(self):
		"""
		Displays the page view a Patient's details
		"""
		# Ensure that the user is authroised to access this page, otherwise redirect to other page
		userType = session['userType'] 
		if userType!= "Health Staff":
			flash("Unauthorised to access this content", 'error')
			return redirect('/')

		# Render the page
		return render_template('healthStaff_viewUserDetails.html', userType=userType)
		
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
		if not self.__viewPatientController.verifyPatient(self.__patientNRIC):
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
		patientDetails = self.__viewPatientController.getPatientDetails(self.__patientNRIC)

		# Render the page with patient's details
		return render_template('healthStaff_viewUserDetails.html', userType=userType,
																   patientDetails=patientDetails)

	def displayError(self, response):
		flash(response, 'error')
		return self.displayPage()