from flask import render_template, session, redirect, request, flash
from ..controllers.OrganisationUser_CreateUserController import OrganisationUser_CreateUserController

class OrganisationUser_CreateUserUI:
	# Empty Constructor
	def __init__(self):
		self.RESULT_SUCCESS = "Success"
		self.RESULT_FAILURE_EMPTY_FIELD = "Fields cannot be empty"
		self.RESULT_FAILURE_MOBILE_LENGTH = "Mobile number must be 8 digits"
		self.RESULT_FAILURE_PASSWORD_MISMATCH = "Password fields no not match"
		self.RESULT_FAILURE_DUPLICATE_VALUE = "{}({}) already exists"
		self.RESULT_FAILURE_NONEXISTENT_VALUE = "{}({}) not does exist"
		self.RESULT_FAILURE_UNEXPECTED = "Error creating new account"

	def onSubmit(self, accountType, NRIC, firstName, middleName,
				 lastName, gender, mobile, password, confirmPassword,
				 businessName, licenseNo, organisationName):

		# Store all possible account types
		accountTypes = ['Public',
						'Health Staff',
						'Business',
						'Organisation']

		# IF any fields are empty
		if accountType == "" or NRIC == "" or \
			firstName == "" or middleName == "" or \
			lastName == "" or mobile == "" or \
			password == "" or confirmPassword == "" or \
			gender == "":

			return self.RESULT_FAILURE_EMPTY_FIELD

		# If necessary details for account type is not provided
		if (accountType == accountTypes[1] and licenseNo == "") or \
			(accountType == accountTypes[2] and businessName == "") or \
			(accountType == accountTypes[3] and organisationName == ""):

			return self.RESULT_FAILURE_EMPTY_FIELD

		# Check if mobile number is 8 characters
		if len(str(mobile)) != 8:
			return self.RESULT_FAILURE_MOBILE_LENGTH

		# Check if passwords match
		if password != confirmPassword:
			return self.RESULT_FAILURE_PASSWORD_MISMATCH

		# Create controller object
		controller = OrganisationUser_CreateUserController()

		# Check if NRIC already exists
		if controller.isDuplicateNRIC(NRIC):
			return self.RESULT_FAILURE_DUPLICATE_VALUE.format('NRIC', NRIC)

		if accountType == accountTypes[0]:
			# Attempt to create new user
			if controller.addNewPublicUser(NRIC, firstName, middleName, lastName, 
											gender, mobile, password):
				return self.RESULT_SUCCESS

		# If Health Staff user
		if accountType == accountTypes[1]:
			if controller.isDuplicateLicenseNo(licenseNo):
				return self.RESULT_FAILURE_DUPLICATE_VALUE.format('License Number', licenseNo)

			if controller.addNewHealthStaffUser(NRIC, firstName, middleName, lastName,
												gender, mobile, password, licenseNo):
				return self.RESULT_SUCCESS

		# If Business User
		if accountType == accountTypes[2]:
			# Check if Business Name is related to a business ID
			businessID = controller.getBusinessID(businessName)
			if businessID == -1:
				return self.RESULT_FAILURE_NONEXISTENT_VALUE.format('Business Name', businessName)

			if controller.addNewBusinessUser(NRIC, firstName, middleName, lastName, 
											gender, mobile, password, businessID):
				return self.RESULT_SUCCESS
			
		# If Organisation user
		if accountType == accountTypes[3]:
			# Check if Organisation Name is related to a organisation ID
			organisationID = controller.getOrganisationID(organisationName)
			if organisationID == -1:
				return self.RESULT_FAILURE_NONEXISTENT_VALUE.format('Organisation Name', organisationName)

			if controller.addNewOrganisationUser(NRIC, firstName, middleName,
												lastName, gender, mobile,
												password, organisationID):
				return self.RESULT_SUCCESS
		
		return self.RESULT_FAILURE_UNEXPECTED

	def displayPage(self):
		"""
		Displays the page to create a user account
		"""
		# Ensure that the user is authroised to access this page, otherwise redirect to other page
		userType = session['userType']
		if userType != "Organisation":
			flash("Unauthorised to access this content", 'error')
			return redirect('/')
		
		# Create Controller Object
		controller = OrganisationUser_CreateUserController()
		businesses = controller.getBusinessNames()
		organisations = controller.getOrganisationNames()
		print(organisations)

		# Render the web page
		return render_template('organisationUser_createUserAccount.html', userType=session['userType'],
																		  businesses=businesses,
																		  organisations=organisations)

	def displaySuccess(self):
		flash("Account created successfully", 'message')
		return redirect(request.url)

	def displayFailure(self, message):
		flash(message, 'error')
		return redirect(request.url)
