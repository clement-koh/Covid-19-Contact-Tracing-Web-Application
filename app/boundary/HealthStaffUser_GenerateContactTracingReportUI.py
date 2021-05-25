from flask import session, flash, redirect, render_template
from ..controllers.HealthStaffUser_GenerateContactTracingReportController import HealthStaffUser_GenerateContactTracingReportController


class HealthStaffUser_GenerateContactTracingReportUI:
	# Constructor
	def __init__(self):
		# Define responses status for the class
		self.RESPONSE_SUCCESS = "Success"
		self.RESPONSE_FAILURE_EMPTY_FIELD = "Date field cannot be empty"

		# Private instance variable
		self.__date = None 		# date
		self.__controller = HealthStaffUser_GenerateContactTracingReportController()	# Controller Object

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
		return render_template('healthStaff_generateContactTracingReport.html', userType=userType,
																 				patientDetails=None,
																 				date=None)
		
	def onSubmit(self, date):
		"""
		Firstly, verify the input field is empty, then check if date exists
		Return a response based on the outcome of each check.
		"""
		# Store the date in private variable
		self.__date = date

		# Check if date field is empty
		if self.__date is None or len(self.__date) == 0:
			return self.RESPONSE_FAILURE_EMPTY_FIELD
		
		# If all checks successful
		return self.RESPONSE_SUCCESS

	def displaySuccess(self):
		"""
		Displays a success page showing the patient's details
		"""
		# Ensure that the user is authroised to access this page, otherwise redirect to other page
		userType = session['userType'] 
		if userType!= "Health Staff":
			flash("Unauthorised to access this content", 'error')
			return redirect('/')

		# Get the details of the infected people
		patientDetails = self.__controller.getInfectedPeopleDetails(self.__date)

		# Render the page with patient's details
		return render_template('healthStaff_generateContactTracingReport.html', userType=userType,
																  				patientDetails=patientDetails, 
																  				date=self.__date)

	def displayError(self, response):
		flash(response, 'error')
		return self.displayPage()