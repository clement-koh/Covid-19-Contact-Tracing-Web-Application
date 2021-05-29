from flask import render_template, session, redirect, request, flash
import re
from ..controllers.OrganisationUser_CreateUserController import OrganisationUser_CreateUserController

class OrganisationUser_CreateUserUI:
	# Empty Constructor
	def __init__(self):
		self.ERROR = ""
		self.RESULT_SUCCESS = "Success"
		self.RESULT_FAILURE_DUPLICATE_VALUE = "{}({}) already exists"
		self.RESULT_FAILURE_NONEXISTENT_VALUE = "{}({}) not does exist"
		self.RESULT_FAILURE_UNEXPECTED = "Error creating new account"
		self.__accountTypes = ['Public', 'Health Staff', 'Business', 'Organisation']

	def __checkFieldsNotEmpty(self, accountType, NRIC, firstName, middleName,
					 	lastName, gender, mobile, password, confirmPassword):
		# Check for empty fields
		if accountType == "" or NRIC == "" or \
			firstName == "" or middleName == "" or \
			lastName == "" or mobile == "" or \
			password == "" or confirmPassword == "" or \
			gender == "":
			
			self.ERROR = "Fields cannot be empty"
			return False

		return True
	
	def __checkRequiredInfoNotEmpty(self, accountType, businessName, licenseNo, organisationName):
		# Check if required info for account type is provided
		if (accountType == self.__accountTypes[1] and licenseNo == "") or \
			(accountType == self.__accountTypes[2] and businessName == "") or \
			(accountType == self.__accountTypes[3] and organisationName == ""):
			
			self.ERROR = "Fields cannot be empty"
			return False

		return True
	
	def __checkIsValidNRIC(self, NRIC):
		# Check if NRIC is starts with S or T and has 3 digits after
		if not re.search('^[S|T][0-9]{4}$', NRIC.upper()):
			self.ERROR = "An invalid NRIC was provided"
			return False
		return True

	def __checkIsValidFullName(self, firstName, middleName, lastName):
		# Check first name, middle name, and last name
		if not re.search('^[A-Z][a-z]+$', firstName) or \
			not re.search('^[A-Z][a-z]+$', middleName) or \
			not re.search('^[A-Z][a-z]+$', lastName):
			self.ERROR = "Name contain invalid characters or does not start with an uppercase alphabet"
			return False

		return True

	def __checkIsValidMobile(self, mobile):
		# Check if mobile number is 8 characters
		if not re.search('^[8|9][0-9]{7}$', mobile):
			self.ERROR = "Mobile number is invalid or not 8 digits"
			return False
		return True

	def __checkIsValidPassword(self, password, confirmPassword):
		# Check if passwords match
		if password != confirmPassword:
			self.ERROR = "Password fields do not match"
			return False

		return True

	def __checkIsValidLicenseNumber(self, accountType, licenseNo):
		# Check if license number is valid
		if (accountType == self.__accountTypes[1]):
			if (len(licenseNo) != 8):
				self.ERROR = "License should be 8 characters"
				return False
			
		return True

	def __createByAccountType(self, accountType, NRIC, firstName, middleName,
							  lastName, gender, mobile, password,
				 			  businessName, licenseNo, organisationName):

		# Create controller object
		controller = OrganisationUser_CreateUserController()

		# Check if NRIC already exists
		if controller.isDuplicateNRIC(NRIC):
			return self.RESULT_FAILURE_DUPLICATE_VALUE.format('NRIC', NRIC)

		if accountType ==self.__accountTypes[0]:
			# Attempt to create new user
			if controller.addNewPublicUser(NRIC, firstName, middleName, lastName, 
											gender, mobile, password):
				return self.RESULT_SUCCESS

		# If Health Staff user
		if accountType ==self.__accountTypes[1]:
			if controller.isDuplicateLicenseNo(licenseNo):
				return self.RESULT_FAILURE_DUPLICATE_VALUE.format('License Number', licenseNo)

			if controller.addNewHealthStaffUser(NRIC, firstName, middleName, lastName,
												gender, mobile, password, licenseNo):
				return self.RESULT_SUCCESS

		# If Business User
		if accountType ==self.__accountTypes[2]:
			# Check if Business Name is related to a business ID
			businessID = controller.getBusinessID(businessName)
			if businessID == -1:
				return self.RESULT_FAILURE_NONEXISTENT_VALUE.format('Business Name', businessName)

			if controller.addNewBusinessUser(NRIC.upper(), firstName, middleName, lastName, 
											gender, mobile, password, businessID):
				return self.RESULT_SUCCESS
			
		# If Organisation user
		if accountType ==self.__accountTypes[3]:
			# Check if Organisation Name is related to a organisation ID
			organisationID = controller.getOrganisationID(organisationName)
			if organisationID == -1:
				return self.RESULT_FAILURE_NONEXISTENT_VALUE.format('Organisation Name', organisationName)

			if controller.addNewOrganisationUser(NRIC, firstName, middleName,
												lastName, gender, mobile,
												password, organisationID):
				return self.RESULT_SUCCESS
		
		return self.RESULT_FAILURE_UNEXPECTED

	def onSubmit(self, accountType, NRIC, firstName, middleName,
				 lastName, gender, mobile, password, confirmPassword,
				 businessName, licenseNo, organisationName):
		if self.__checkFieldsNotEmpty(accountType, NRIC, firstName, middleName,
					 				  lastName, gender, mobile, password, confirmPassword) and \
			self.__checkRequiredInfoNotEmpty(accountType, businessName, licenseNo, organisationName) and \
			self.__checkIsValidNRIC(NRIC) and \
			self.__checkIsValidFullName(firstName, middleName, lastName) and \
			self.__checkIsValidMobile(mobile) and \
			self.__checkIsValidPassword(password, confirmPassword) and \
			self.__checkIsValidLicenseNumber(accountType, licenseNo):

			# Check the account type and update the user accordingly
			return self.__createByAccountType(accountType, NRIC, firstName, middleName,
											  lastName, gender, mobile, password,
											  businessName, licenseNo, organisationName)

		return self.ERROR
		

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
