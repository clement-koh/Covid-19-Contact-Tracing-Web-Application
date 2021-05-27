from flask import render_template, request, send_from_directory, flash, jsonify, session
from ..run import app, loginRequired

# Boundary for Users
from .boundary.User_LoginUI import User_LoginUI
from .boundary.User_LogoutUI import User_LogoutUI
from .boundary.User_UpdateContactUI import User_UpdateContactUI
from .boundary.User_ChangePasswordUI import User_ChangePasswordUI

# Boundary for Public Users
from .boundary.PublicUser_ExposureStatusUI import PublicUser_ExposureStatusUI
from .boundary.PublicUser_ViewLocationHistoryUI import PublicUser_ViewLocationHistoryUI
from .boundary.PublicUser_ViewAffectedLocationUI import PublicUser_ViewAffectedLocationUI
from .boundary.PublicUser_ViewAlertUI import PublicUser_ViewAlertUI
from .boundary.PublicUser_AcknowledgeAlertUI import PublicUser_AcknowledgeAlertUI
from .boundary.PublicUser_ViewVaccineCertificateUI import PublicUser_ViewVaccineCertificateUI

# Boundary for Health Staff
from .boundary.HealthStaffUser_ViewPatientDetailsUI import HealthStaffUser_ViewPatientDetailsUI
from .boundary.HealthStaffUser_SendAlertPublicUI import HealthStaffUser_SendAlertPublicUI
from .boundary.HealthStaffUser_SendAlertBusinessUI import HealthStaffUser_SendAlertBusinessUI
from .boundary.HealthStaffUser_ViewVaccineStatusUI import HealthStaffUser_ViewVaccineStatusUI
from .boundary.HealthStaffUser_UpdateVaccinationUI import HealthStaffUser_UpdateVaccinationUI
from .boundary.HealthStaffUser_GenerateContactTracingReportUI import HealthStaffUser_GenerateContactTracingReportUI

# Boundary for Business Staff
from .boundary.BusinessUser_ViewAlertUI import BusinessUser_ViewAlertUI
from .boundary.BusinessUser_AcknowledgeAlertUI import BusinessUser_AcknowledgeAlertUI
from .boundary.BusinessUser_ViewAffectedOutletUI import BusinessUser_ViewAffectedOutletUI

# Boundary for Organisation Staff
from .boundary.OrganisationUser_CreateUserUI import OrganisationUser_CreateUserUI
from .boundary.OrganisationUser_ViewUserAccountUI import OrganisationUser_ViewUserAccountUI
from .boundary.OrganisationUser_UpdateUserAccountUI import OrganisationUser_UpdateUserAccountUI
from .boundary.OrganisationUser_SuspendUserAccountUI import OrganisationUser_SuspendUserAccountUI
from .boundary.OrganisationUser_GenerateVaccinationStatusReportUI import OrganisationUser_GenerateVaccinationStatusReportUI
from .boundary.OrganisationUser_GenerateInfectionReportUI import OrganisationUser_GenerateInfectionReportUI


# -----------------------------------------------------
#                   Common Pages
# -----------------------------------------------------
@app.route('/', methods=['GET'])
@loginRequired
def overviewPage():
	# Create PublicUser_ExposureStatusBoundary Object
	publicUser_exposureStatusBoundary = PublicUser_ExposureStatusUI()

	# Exposure status is none if user is not a public user
	exposureStatus = publicUser_exposureStatusBoundary.getExposureStatus()

	# Displays the webpage
	return render_template('overview.html', userType = session['userType'],
											healthStatus = exposureStatus)

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
	print("Enter Login Page")
	# Initialise User_LoginUI Object
	user_loginBoundary = User_LoginUI()

	# If user is requesting the page
	if request.method == 'GET':
		# If user is already logged in, redirect to main page
		# accessing the /login directly into address bar after logged in already
		if user_loginBoundary.checkUserLoggedIn():
			return user_loginBoundary.displaySuccess()

		# Else if user is not logged in, show login screen
		return user_loginBoundary.displayPage()

	# If user is submitting the login details
	if request.method == "POST":
		# Get fields from the login form
		username = request.form['username'].upper()
		password = request.form['password']

		# If login fields are empty
		if user_loginBoundary.isLoginFieldsEmpty(username, password):
			message = "Username and password must not be empty"
			return user_loginBoundary.displayError(message=message)
		
		# Submit the data
		response = user_loginBoundary.onSubmit(username, password)
		
		# IF response is successful
		if response ==  user_loginBoundary.RESPONSE_SUCCESS:
			return user_loginBoundary.displaySuccess()
		else:
			return user_loginBoundary.displayError(message=response)


@app.route('/logout', methods=['GET'])
@loginRequired
def logout():
	# Initialise User_LogoutUI Object
	user_logoutBoundary = User_LogoutUI()

	# Log User Out
	user_logoutBoundary.logout()

	# Redirect to login page
	return user_logoutBoundary.redirectToLogin()
		

@app.route('/update_contact', methods=['GET', 'POST'])
@loginRequired
def updateContactPage():
	# Initialise User_UpdateContactUI Object
	user_updateContactBoundary = User_UpdateContactUI()
	
	# If user is requesting the page
	if request.method == 'GET':
		# Display the requested page
		return user_updateContactBoundary.displayPage()

	# If user is submitting new details to be updated
	if request.method == 'POST':

		# Get fields from the update contact form
		mobile = request.form['mobile']

		# If unsuccessful at updating mobile number
		if not user_updateContactBoundary.onSubmit(mobile):
			error_message = "Failed to update mobile number" 
			return user_updateContactBoundary.displayError(message=error_message)
		
		# If successful at updating mobile number
		return user_updateContactBoundary.displaySuccess()

@app.route('/settings', methods=['GET', 'POST'])
@loginRequired
def settingsPage():
	# Initialise User_ChangePasswordUI Object
	user_changePasswordBoundary = User_ChangePasswordUI()

	# If user is requesting the page
	if request.method == 'GET':
		# Display the requested page
		return user_changePasswordBoundary.displayPage()

	# If user is submitting new details to be updated
	if request.method == 'POST':

		# Get fields from the update contact form
		oldPassword = request.form['current_pw']
		newPassword = request.form['new_pw']
		newPassword2 = request.form['new_pw2']

		# Check if fields are empty
		if user_changePasswordBoundary.isFieldsEmpty(oldPassword, newPassword, newPassword2):
			# Display error message if fields are empty
			error_message = "Fields cannot be empty"
			return user_changePasswordBoundary.displayError(message=error_message)

		# Check if passwords do not match
		if not user_changePasswordBoundary.isMatchingPassword(newPassword, newPassword2):
			# Display error message if new password does not match
			error_message = "New Password and Confirm New Password does not match"
			return user_changePasswordBoundary.displayError(message=error_message)

		# If unsuccessful at compare old password and updating
		if not user_changePasswordBoundary.onSubmit(oldPassword, newPassword):
			error_message = "Current Password is incorrect" 
			return user_changePasswordBoundary.displayError(message=error_message)
		
		# If successful at updating
		return user_changePasswordBoundary.displaySuccess()

# -----------------------------------------------------
#                   Public User Pages
# -----------------------------------------------------
@app.route('/view_alert', methods=['GET', 'POST'])
@loginRequired
def viewAlertPage():
	# If user is requesting the page
	if request.method == 'GET':
		# Initialize boundary object to view alert
		publicUser_viewAlertBoundary = PublicUser_ViewAlertUI()

		# Display the requested page
		return publicUser_viewAlertBoundary.displayPage()

	# Update mark as read first
	if request.method == 'POST':
		# Get the id of the alert being marked as read
		id = request.form['alert_id']

		# Initialize boundary obect to acknowledge alert
		publicUser_acknowledgeAlertBoundary = PublicUser_AcknowledgeAlertUI()

		# Attempt to update status of alert in database
		response = publicUser_acknowledgeAlertBoundary.onSubmit(id)

		# If submission is unsuccessful
		if response == publicUser_acknowledgeAlertBoundary.RESPONSE_FAILURE:
			return publicUser_acknowledgeAlertBoundary.displayError()
		
		# If submission is successful
		return publicUser_acknowledgeAlertBoundary.displaySuccess()


@app.route('/view_location_history', methods=['GET'])
@loginRequired
def viewLocationHistoryPage():
	# Initialise User_ChangePasswordUI Object
	publicUser_viewLocationHistoryBoundary = PublicUser_ViewLocationHistoryUI()

	return publicUser_viewLocationHistoryBoundary.displayPage()

@app.route('/view_affected_location', methods=['GET', 'POST'])
@loginRequired
def viewAffectedLocationPage():
	# Initialise PublicUser_ViewAffectedLocationUI Object
	publicUser_viewAffectedLocationBoundary = PublicUser_ViewAffectedLocationUI()

	# If user is requesting the page
	if request.method == 'GET':
		return publicUser_viewAffectedLocationBoundary.displayPage()

	# Provide data back based on an ajax call
	if request.method == 'POST':
		days_ago = int(request.form['days_ago'])
		return publicUser_viewAffectedLocationBoundary.getAffectedLocation(days_ago)

@app.route('/view_vaccine_certificate', methods=['GET'])
@loginRequired
def viewVaccineCertificate():
	publicUser_viewVaccineCertificateBoundary = PublicUser_ViewVaccineCertificateUI()
	return publicUser_viewVaccineCertificateBoundary.displayPage()

# -----------------------------------------------------
#                   Health Staff Pages
# -----------------------------------------------------
@app.route('/send_public_alert', methods=['GET', 'POST'])
@loginRequired
def sendPublicAlertPage():
	# Initialise Boundary Object
	healthStaffUser_sendAlertPublicBoundary = HealthStaffUser_SendAlertPublicUI()

	# If user is requesting the page
	if request.method == 'GET':
	
		# Display the requested page
		return healthStaffUser_sendAlertPublicBoundary.displayPage()

	# If user is submitting alert information
	if request.method == 'POST':

		# Get form details
		recipient = request.form['target'].strip()
		message = request.form['message'].strip()

		# Get result of trying to send alert
		result = healthStaffUser_sendAlertPublicBoundary.onSubmit(recipient, message)

		# Display result if not successful
		if result != healthStaffUser_sendAlertPublicBoundary.RESPONSE_SUCCESS:
			return healthStaffUser_sendAlertPublicBoundary.displayError(result)

		# Else display success
		return healthStaffUser_sendAlertPublicBoundary.displaySuccess()

@app.route('/send_business_alert', methods=['GET', 'POST'])
@loginRequired
def sendBusinessAlertPage():
	# Initialise Boundary Object
	healthStaffUser_sendAlertBusinessBoundary = HealthStaffUser_SendAlertBusinessUI()

	# If user is requesting the page
	if request.method == 'GET':
	
		# Display the requested page
		return healthStaffUser_sendAlertBusinessBoundary.displayPage()

	# If user is submitting alert information
	if request.method == 'POST':

		# Get form details
    
		recipient = request.form['target'].strip()
		message = request.form['message'].strip()

		# Get result of trying to send alert
		result = healthStaffUser_sendAlertBusinessBoundary.onSubmit(recipient, message)

		# Display result if not successful
		if result != healthStaffUser_sendAlertBusinessBoundary.RESPONSE_SUCCESS:
			return healthStaffUser_sendAlertBusinessBoundary.displayError(result)

		# Else display success
		return healthStaffUser_sendAlertBusinessBoundary.displaySuccess()


@app.route('/view_patient_details', methods=['GET', 'POST'])
@loginRequired
def viewPatientDetailsPage():
	# Initialise Boundary Object
	healthStaffUser_viewPatientDetailsBoundary = HealthStaffUser_ViewPatientDetailsUI()

	# If user is requesting the page
	if request.method == 'GET':
		# Display the requested page
		return healthStaffUser_viewPatientDetailsBoundary.displayPage()

	if request.method == 'POST':
		# Get form details
		NRIC = request.form['user'].strip()

		# Get submit response 
		response = healthStaffUser_viewPatientDetailsBoundary.onSubmit(NRIC)

		# Display Error if any
		if response != healthStaffUser_viewPatientDetailsBoundary.RESPONSE_SUCCESS:
			return healthStaffUser_viewPatientDetailsBoundary.displayError(response)

		# Display Success
		return healthStaffUser_viewPatientDetailsBoundary.displaySuccess()

@app.route('/view_update_vaccination', methods=['GET', 'POST'])
@loginRequired
def viewUpdateVaccination():
	# Initialise Boundary Object
	healthStaffUser_viewVaccineStatusBoundary = HealthStaffUser_ViewVaccineStatusUI()

	if request.method == 'GET':
		# Display the requested page
		return healthStaffUser_viewVaccineStatusBoundary.displayPage()

	if request.method == 'POST':
		# Get form details
		NRIC = request.form['user'].strip()

		# Get submit response 
		response = healthStaffUser_viewVaccineStatusBoundary.onSubmit(NRIC)

		# Display Error if any
		if response != healthStaffUser_viewVaccineStatusBoundary.RESPONSE_SUCCESS:
			return healthStaffUser_viewVaccineStatusBoundary.displayError(response)

		# Display Success
		return healthStaffUser_viewVaccineStatusBoundary.displaySuccess()

@app.route('/update_vaccination', methods=['POST'])
@loginRequired
def UpdateVaccinationPage():

	# Initialise HealthStaffUser_UpdateVaccinationUI Object
	healthStaffUser_UpdateVaccinationBoundary = HealthStaffUser_UpdateVaccinationUI()

	# Get fields from the update vaccination status form
	NRIC = request.form.get('name')
	vaccination_Status = request.form.get('vaccinationstatus')
	first_dose = request.form.get('first_dose')
	second_dose = request.form.get('second_dose')

	# If unsuccessful at updating vaccination status
	if not healthStaffUser_UpdateVaccinationBoundary.onSubmit(NRIC, vaccination_Status, first_dose, second_dose):
		return healthStaffUser_UpdateVaccinationBoundary.displayError()
		
	# If successful at updating vaccination status
	return healthStaffUser_UpdateVaccinationBoundary.displaySuccess()
	
@app.route('/contact_tracing', methods=['GET', 'POST'])
@loginRequired
def contactTracingPage():
	# Initialise Boundary Object
	healthStaffUser_GenerateContactTracingReportBoundary = HealthStaffUser_GenerateContactTracingReportUI()

	# If user is requesting the page
	if request.method == 'GET':
		# Display the requested page
		return healthStaffUser_GenerateContactTracingReportBoundary.displayPage()

	if request.method == 'POST':
		# Get form details
		date = request.form['date'].strip()

		# Get submit response 
		response = healthStaffUser_GenerateContactTracingReportBoundary.onSubmit(date)

		# Display Error if any
		if response != healthStaffUser_GenerateContactTracingReportBoundary.RESPONSE_SUCCESS:
			return healthStaffUser_GenerateContactTracingReportBoundary.displayError(response)

		# Display Success
		return healthStaffUser_GenerateContactTracingReportBoundary.displaySuccess()			

# -----------------------------------------------------
#                   Business User Pages
# -----------------------------------------------------
@app.route('/view_business_alert', methods=['GET', 'POST'])
@loginRequired
def viewBusinessAlertPage():
	# If user is requesting the page
	if request.method == 'GET':
		# Initialize boundary object to view alert
		businessUser_viewAlertBoundary = BusinessUser_ViewAlertUI()

		# Display the requested page
		return businessUser_viewAlertBoundary.displayPage()

	# Update mark as read first
	if request.method == 'POST':
		# Get the id of the alert being marked as read
		id = request.form['alert_id']

		# Initialize boundary obect to acknowledge alert
		businessUser_acknowledgeAlertBoundary = BusinessUser_AcknowledgeAlertUI()

		# Attempt to update status of alert in database
		response = businessUser_acknowledgeAlertBoundary.onSubmit(id)

		# If submission is unsuccessful
		if response == businessUser_acknowledgeAlertBoundary.RESPONSE_FAILURE:
			return businessUser_acknowledgeAlertBoundary.displayError()
		
		# If submission is successful
		return businessUser_acknowledgeAlertBoundary.displaySuccess()

@app.route('/view_affected_outlet', methods=['GET'])
@loginRequired
def viewAffectedOutlet():
	businessUser_viewAffectedOutletBoundary = BusinessUser_ViewAffectedOutletUI()
	return businessUser_viewAffectedOutletBoundary.displayPage()


# -----------------------------------------------------
#                   Organisation User Pages
# -----------------------------------------------------
@app.route('/create_user_account', methods=['GET', 'POST'])
@loginRequired
def CreateUserAccount():
	# Create boundary object
	organisationUser_createUserBoundary = OrganisationUser_CreateUserUI()

	# If user is requesting the web page
	if request.method == 'GET':
		return organisationUser_createUserBoundary.displayPage()
	
	# If user is submitting request to create a new account
	if request.method == 'POST':

		# Gets all form data, set to empty string if field is disabled
		accountType = request.form.get('accountType')
		NRIC = request.form.get('NRIC', '').strip().upper()
		firstName = request.form.get('firstName', '').strip()
		middleName = request.form.get('middleName', '').strip()
		lastName = request.form.get('lastName', '').strip()
		gender = request.form.get('gender')
		mobile = request.form.get('mobile', '').strip()
		password = request.form.get('password', '').strip()
		confirmPassword = request.form.get('confirmPassword', '').strip()
		businessName = request.form.get('businessName', '').strip()
		licenseNo = request.form.get('licenseNo', '').strip()
		organisationName = request.form.get('organisationName', '').strip()

		result = organisationUser_createUserBoundary.onSubmit(accountType, NRIC, firstName, middleName, 
															  lastName, gender, mobile, password, confirmPassword,
															  businessName, licenseNo, organisationName)
		
		# If attempt to create account is successful
		if result == organisationUser_createUserBoundary.RESULT_SUCCESS:
			return organisationUser_createUserBoundary.displaySuccess()
		
		# Display Error if account creation is unsuccessful
		return organisationUser_createUserBoundary.displayFailure(result)

@app.route('/view_user_account', methods=['GET', 'POST'])
@loginRequired
def ViewUserAccount():
	# Initialise Boundary Object
	organisationUser_viewUserBoundary = OrganisationUser_ViewUserAccountUI()

	if request.method == 'GET':
		# Display the requested page
		return organisationUser_viewUserBoundary.displayPage()

	if request.method == 'POST':
		# Get form details
		NRIC = request.form['user'].strip()

		# Get submit response 
		response = organisationUser_viewUserBoundary.onSubmit(NRIC)

		# Display Error if any
		if response != organisationUser_viewUserBoundary.RESPONSE_SUCCESS:
			return organisationUser_viewUserBoundary.displayError(response)
			
		# Display Success
		return organisationUser_viewUserBoundary.displaySuccess()


@app.route('/update_user_account', methods=['GET', 'POST'])
@loginRequired
def UpdateUserAccount(): 
	# Create boundary object
	organisationUser_updateUserAccountBoundary = OrganisationUser_UpdateUserAccountUI()

	if request.method == 'GET':
		NRIC = request.args.get('NRIC')
		return organisationUser_updateUserAccountBoundary.displayPage(NRIC)
	
	if request.method == 'POST':
		accountType = request.form.get('accountType')
		NRIC = request.form.get('NRIC')
		firstName = request.form.get('firstName', '').strip()
		middleName = request.form.get('middleName', '').strip()
		lastName = request.form.get('lastName', '').strip()
		gender = request.form.get('gender')
		mobile = request.form.get('mobile', '').strip()
		password = request.form.get('password', '').strip()
		confirmPassword = request.form.get('confirmPassword', '').strip()
		businessName = request.form.get('businessName', '').strip()
		licenseNo = request.form.get('licenseNo', '').strip()
		organisationName = request.form.get('organisationName', '').strip()

		result = organisationUser_updateUserAccountBoundary.onSubmit(accountType, NRIC, firstName, middleName,
																	 lastName, gender, mobile, password, confirmPassword,
																	 businessName, licenseNo, organisationName)
		
		# If attempt to update account is successful
		if result == organisationUser_updateUserAccountBoundary.RESULT_SUCCESS:
			return organisationUser_updateUserAccountBoundary.displaySuccess(NRIC)

		# Display error message if update is unsuccessful
		return organisationUser_updateUserAccountBoundary.displayError(NRIC, result)

@app.route('/suspend_user_account', methods=['POST'])
@loginRequired
def SuspendUserAccount():

	# Initialise OrganisationUser_SuspendUserAccountUI Object
	OrganisationUser_SuspendAccountBoundary = OrganisationUser_SuspendUserAccountUI()
	
	# Get fields from the view User Account form
	NRIC = request.form.get('NRIC')

	# If unsuccessful at updating Account Status
	if not OrganisationUser_SuspendAccountBoundary.onSubmit(NRIC):
		return OrganisationUser_SuspendAccountBoundary.displayError()
		
	# If successful at updating Account Status
	return OrganisationUser_SuspendAccountBoundary.displaySuccess()

@app.route('/view_vaccination_report', methods=['GET'])
@loginRequired
def ViewVaccinationStatusReport():
	# Create boundary object
	organisationUser_generateVaccinationStatusReportBoundary = OrganisationUser_GenerateVaccinationStatusReportUI()
	return organisationUser_generateVaccinationStatusReportBoundary.displayPage()

@app.route('/view_infection_report', methods=['GET', 'POST'])
@loginRequired
def viewStatisticReport():

	# Initialise OrganisationUser_SuspendUserAccountUI Object
	organisationUser_generateInfectionReportBoundary = OrganisationUser_GenerateInfectionReportUI()

	if request.method == 'GET':
		# Display the requested page
		return organisationUser_generateInfectionReportBoundary.displayPage()

	if request.method == 'POST':
		# Display the requested page
		days_ago = int(request.form['days_ago'])
		return organisationUser_generateInfectionReportBoundary.getAffectedLocation(days_ago)