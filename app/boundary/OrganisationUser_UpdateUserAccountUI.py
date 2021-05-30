from flask import render_template, session, redirect, url_for, request, flash
import re
from ..controllers.OrganisationUser_UpdateUserAccountController import OrganisationUser_UpdateUserAccountController

class OrganisationUser_UpdateUserAccountUI:
	# Empty constructor
	def __init__(self):
		self.RESULT_SUCCESS = "Success"
		self.ERROR = ""
		self.RESULT_FAILURE_DUPLICATE_VALUE = "{}({}) already exists"
		self.RESULT_FAILURE_NONEXISTENT_VALUE = "{}({}) does not exist"
		self.__controller = OrganisationUser_UpdateUserAccountController()
		self.__accountTypes = ['Public', 'Business', 'Health Staff', 'Organisation']

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
		if (accountType == self.__accountTypes[1] and businessName == "") or \
			(accountType == self.__accountTypes[2] and licenseNo == "") or \
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
		if (accountType == self.__accountTypes[2]):
			if (len(licenseNo) != 8):
				self.ERROR = "License should be 8 characters"
				return False
			
		return True

	def __updateByAccountType(self, accountType, NRIC, firstName, middleName,
							  lastName, gender, mobile, password,
				 			  businessName, licenseNo, organisationName):

		# Get current user data
		userInfo = self.__controller.getUserDetails(NRIC)

		# Is account type is public user
		if accountType == self.__accountTypes[0]:
			# Attempt to update the user
			if self.__controller.updatePublicUser(NRIC, firstName, middleName, lastName,
											gender, mobile, password):
				return self.RESULT_SUCCESS
		
		# Is account type is business user
		if accountType == self.__accountTypes[1]:
			# Check if business name is related to a business ID
			businessID = self.__controller.getBusinessID(businessName)
			if businessID == -1:

				return self.RESULT_FAILURE_NONEXISTENT_VALUE.format('Business Name', businessName)

			# Attempt to update the business user
			if self.__controller.updateBusinessUser(NRIC, firstName, middleName, lastName,
											 gender, mobile, password, businessName):
				return self.RESULT_SUCCESS

		# Is account type is health staff user
		if accountType == self.__accountTypes[2]:
			if str(licenseNo) != str(userInfo[9]):
				# Check if license number already exists
				if self.__controller.isDuplicateLicenseNo(licenseNo):
					return self.RESULT_FAILURE_DUPLICATE_VALUE.format('License Number', licenseNo)

			# Attempt to update the health staff user
			if self.__controller.updateHealthStaffUser(NRIC, firstName, middleName, lastName,
												gender, mobile, password, licenseNo):
				return self.RESULT_SUCCESS

		# Is account type is organisation user
		if accountType == self.__accountTypes[3]:
			# Check if organisation name is related to an organisation ID
			organisationID = self.__controller.getOrganisationID(organisationName)
			if organisationID == -1:
				return self.RESULT_FAILURE_NONEXISTENT_VALUE.format('Organisation Name', organisationName)
			
			# Attempt to update the organisation user
			if self.__controller.updateOrganisationUser(NRIC, firstName, middleName, lastName,
												 gender, mobile, password, organisationID):
				return self.RESULT_SUCCESS

	def displayPage(self, NRIC):
		"""
		Display the page to update a user account
		"""
		# Ensure the user is authorised to view the page
		userType = session['userType']
		if userType != "Organisation":
			flash("Unauthorised access to this content", "error")
			return redirect("/")
		
		userInfo = self.__controller.getUserDetails(NRIC)
		businesses = self.__controller.getBusinessNames()
		organisations = self.__controller.getOrganisationNames()

		# Render the web page
		return render_template('organisationUser_updateUserAccount.html', userType=userType,
																		  userInfo=userInfo,
																		  businesses=businesses,
																		  organisations=organisations)

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
			return self.__updateByAccountType(accountType, NRIC, firstName, middleName,
										lastName, gender, mobile, password,
										businessName, licenseNo, organisationName)

		return self.ERROR

	def displaySuccess(self, NRIC):
		flash("Account updated successfully", "message")
		print(request.url)
		return redirect(url_for('UpdateUserAccount', NRIC=NRIC))

	def displayError(self, NRIC, error):
		flash(error, "error")
		return redirect(url_for('UpdateUserAccount', NRIC=NRIC))