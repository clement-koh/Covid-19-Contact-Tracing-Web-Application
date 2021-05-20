from flask import session, flash, redirect, render_template
from ..controllers.HealthStaffUser_ContactTracingController import HealthStaffUser_ContactTracingController


class HealthStaffUser_ContactTracingUI:
	# Constructor
	def __init__(self):
		# Define responses status for the class
		self.RESPONSE_SUCCESS = "Success"
		self.RESPONSE_FAILURE_EMPTY_FIELD = "Date field cannot be empty"

		# Private instance variable
		self.__date = None 														# date
		self.__viewPatientContactTracingController = HealthStaffUser_ContactTracingController()	# Controller Object

	# Mutator Method
	def setDate(self, date):
		self.__date = date

	# Other Method
	def displayPage(self):
		"""
		Displays the page view with Patient's details
		"""
		# Ensure that the user is authroised to access this page, otherwise redirect to other page
		userType = session['userType'] 
		if userType!= "Health Staff":
			flash("Unauthorised to access this content", 'error')
			return redirect('/')

		# Render the page
		return render_template('healthStaff_ContactTracing.html', userType=userType)
		
	def onSubmit(self):
		"""
		Firstly, verify the input field is empty, then check if date exists
		Return a response based on the outcome of each check.
		"""
		# Check if date field is empty
		if self.__date is None or len(self.__date) == 0:
			return self.RESPONSE_FAILURE_EMPTY_FIELD
		
		# If all checks successful
		return self.RESPONSE_SUCCESS

	def displaySuccess(self):
		"""
		Displays a success page showing the patient's details
		"""
		# gets the current user type
		userType = session['userType']

		# get date
		date = self.__date

		# get list of nric of infected people for last 14 days 
		NRIClist = self.__viewPatientContactTracingController.getInfectedPeopleNRIC(self.__date)
		
		# get the patient's details
		patientDetails = self.__viewPatientContactTracingController.getPatientDetails(NRIClist)

		# Render the page with patient's details
		return render_template('healthStaff_ContactTracing.html', userType=userType,
																   patientDetails=patientDetails, date=date)

	def displayError(self, response):
		flash(response, 'error')
		return self.displayPage()