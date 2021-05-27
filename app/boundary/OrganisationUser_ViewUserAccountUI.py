from flask import session, flash, redirect, render_template
from ..controllers.OrganisationUser_ViewUserAccountController import OrganisationUser_ViewUserAccountController
class OrganisationUser_ViewUserAccountUI:
	# Constructor
	def __init__(self):
		# Define responses status for the class
		self.RESPONSE_SUCCESS = "Success"
		self.RESPONSE_FAILURE_EMPTY_FIELD = "NRIC field cannot be empty"
		self.RESPONSE_FAILURE_INVALID_NRIC = "Invalid NRIC"

		# Private instance variable
		self.__userNRIC = None 														# User's NRIC Number
		self.__viewUserAccountController = OrganisationUser_ViewUserAccountController()	# Controller Object	


	# Other Method
	def displayPage(self):
		"""
		Displays the page view a User's details
		"""
		# Ensure that the user is authroised to access this page, otherwise redirect to other page
		userType = session['userType'] 
		if userType!= "Organisation":
			flash("Unauthorised to access this content", 'error')
			return redirect('/')

		# If directed here with a user already provided
		if session['viewingNRIC'] is not None:
			# Get provided user details
			self.__userNRIC = session['viewingNRIC']

			# Remove user details stored
			session['viewingNRIC'] = None

			# Display information of user
			return self.displaySuccess()

		# Render the page
		return render_template('organisationUser_viewUserAccount.html', userType=userType)
	
	def onSubmit(self, NRIC):
		"""
		Firstly, verify the input field is empty, then check if NRIC exists
		Return a response based on the outcome of each check.
		"""

		self.__userNRIC = NRIC

		# Check if NRIC field is empty
		if self.__userNRIC is None or len(self.__userNRIC) == 0:
			return self.RESPONSE_FAILURE_EMPTY_FIELD
		
		# Check if NRIC exists
		if not self.__viewUserAccountController.verifyUser(self.__userNRIC):
			return self.RESPONSE_FAILURE_INVALID_NRIC
		
		# If all checks successful
		return self.RESPONSE_SUCCESS
	
	def displaySuccess(self):
		"""
		Displays a success page showing the User's details
		"""
		# Gets the current user type
		userType = session['userType']

		# Get the User's details
		userDetails = self.__viewUserAccountController.getUserDetails(self.__userNRIC)

		# Render the page with User's details
		return render_template('organisationUser_viewUserAccount.html', userType=userType,
																   userDetails=userDetails)

	def displayError(self, response):
		flash(response, 'error')
		return self.displayPage()
