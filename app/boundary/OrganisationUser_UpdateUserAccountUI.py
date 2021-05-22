from flask import render_template, session, redirect, url_for, request, flash
import re
from ..controllers.OrganisationUser_UpdateUserAccountController import OrganisationUser_UpdateUserAccountController

class OrganisationUser_UpdateUserAccountUI:
	# Empty constructor
	def __init__(self):
		self.RESULT_SUCCESS = "Success"
		self.RESULT_FAILURE_INVALID_NRIC = "An invalid NRIC was provided"
		self.RESULT_FAILURE_INVALID_NAME = "Name contain invalid characters or does not start with an uppercase alphabet"
		self.RESULT_FAILURE_EMPTY_FIELD = "Fields cannot be empty"
		self.RESULT_FAILURE_MOBILE_LENGTH = "Mobile number is invalid or not 8 digits"
		self.RESULT_FAILURE_PASSWORD_MISMATCH = "Password fields do not match"
		self.RESULT_FAILURE_INVALID_LICENSE = "License should be 8 characters"
		self.RESULT_FAILURE_DUPLICATE_VALUE = "{}({}) already exists"
		self.RESULT_FAILURE_NONEXISTENT_VALUE = "{}({}) does not exist"
		self.RESULT_FAILURE_UNEXPECTED = "An error occurred when updating the account"

	def displayPage(self, NRIC):
		"""
		Display the page to update a user account
		"""
		# Ensure the user is authorised to view the page
		userType = session['userType']
		if userType != "Organisation":
			flash("Unauthorised access to this content", "error")
			return redirect("/")
		
		# Create controller object
		controller = OrganisationUser_UpdateUserAccountController()
		userInfo = controller.getUserDetails(NRIC)
		businesses = controller.getBusinessNames()
		organisations = controller.getOrganisationNames()

		# Render the web page
		return render_template('organisationUser_updateUserAccount.html', userType=userType,
																		  userInfo=userInfo,
																		  businesses=businesses,
																		  organisations=organisations)

	def onSubmit(self, accountType, NRIC, firstName, middleName,
				 lastName, gender, mobile, password, confirmPassword,
				 businessName, licenseNo, organisationName):
		accountTypes = [
			'Public',
			'Business',
			'Health Staff',
			'Organisation'
		]

		# Create controller object
		controller = OrganisationUser_UpdateUserAccountController()
		
		# Get current user data
		userInfo = controller.getUserDetails(NRIC)

		# Check for empty fields
		if accountType == "" or NRIC == "" or \
			firstName == "" or middleName == "" or \
			lastName == "" or mobile == "" or \
			password == "" or confirmPassword == "" or \
			gender == "" :
			
			return self.RESULT_FAILURE_EMPTY_FIELD

		# Check if required info for account type is provided
		if (accountType == accountTypes[1] and businessName == "") or \
			(accountType == accountTypes[2] and licenseNo == "") or \
			(accountType == accountTypes[3] and organisationName == ""):

			return self.RESULT_FAILURE_EMPTY_FIELD

		# Check if NRIC is starts with S or T and has 3 digits after
		if not re.search('^[S|T][0-9]{4}$', NRIC.upper()):
			return self.RESULT_FAILURE_INVALID_NRIC

		# Check first name, middle name, and last name
		if not re.search('^[A-Z][a-z]+$', firstName) or \
			not re.search('^[A-Z][a-z]+$', middleName) or \
			not re.search('^[A-Z][a-z]+$', lastName):
			return self.RESULT_FAILURE_INVALID_NAME

		# Check if mobile number is 8 characters
		if not re.search('^[8|9][0-9]{7}$', mobile):
			return self.RESULT_FAILURE_MOBILE_LENGTH

		# Check if passwords match
		if password != confirmPassword:
			return self.RESULT_FAILURE_PASSWORD_MISMATCH

		# Check if license number is valid
		if (accountType == accountTypes[2]):
			if (len(licenseNo) != 8):
				return self.RESULT_FAILURE_INVALID_LICENSE
		
		# If account type is public user
		if accountType == accountTypes[0]:
			# Attempt to update the user
			if controller.updatePublicUser(NRIC, firstName, middleName, lastName,
											gender, mobile, password):
				return self.RESULT_SUCCESS
		
		# If account type is business user
		if accountType == accountTypes[1]:
			# Check if business name is related to a business ID
			businessID = controller.getBusinessID(businessName)
			if businessID == -1:

				return self.RESULT_FAILURE_NONEXISTENT_VALUE.format('Business Name', businessName)

			# Attempt to update the business user
			if controller.updateBusinessUser(NRIC, firstName, middleName, lastName,
											 gender, mobile, password, businessName):
				return self.RESULT_SUCCESS

		# If account type is health staff user
		if accountType == accountTypes[2]:
			if str(licenseNo) != str(userInfo[9]):
				# Check if license number already exists
				if controller.isDuplicateLicenseNo(licenseNo):
					return self.RESULT_FAILURE_DUPLICATE_VALUE.format('License Number', licenseNo)

			# Attempt to update the health staff user
			if controller.updateHealthStaffUser(NRIC, firstName, middleName, lastName,
												gender, mobile, password, licenseNo):
				return self.RESULT_SUCCESS

		# If account type is organisation user
		if accountType == accountTypes[3]:
			# Check if organisation name is related to an organisation ID
			organisationID = controller.getOrganisationID(organisationName)
			if organisationID == -1:
				return self.RESULT_FAILURE_NONEXISTENT_VALUE.format('Organisation Name', organisationName)
			
			# Attempt to update the organisation user
			if controller.updateOrganisationUser(NRIC, firstName, middleName, lastName,
												 gender, mobile, password, organisationID):
				return self.RESULT_SUCCESS

		return self.RESULT_FAILURE_UNEXPECTED
	
	def displaySuccess(self, NRIC):
		flash("Account updated successfully", "message")
		print(request.url)
		return redirect(url_for('UpdateUserAccount', NRIC=NRIC))

	def displayError(self, NRIC, message):
		flash(message, "error")
		return redirect(url_for('UpdateUserAccount', NRIC=NRIC))