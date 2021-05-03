from flask import render_template, request, send_from_directory, flash, jsonify, session
from ..run import app, loginRequired

# Boundary for Users
from .boundary.User_LoginUI import User_LoginUI
from .boundary.User_LogoutUI import User_LogoutUI
from .boundary.User_UpdateContactUI import User_UpdateContactUI
from .boundary.User_ChangePasswordUI import User_ChangePasswordUI

# Boundary for Public Users
from .boundary.PublicUser_ExposureStatusUI import PublicUser_ExposureStatusUI
from .boundary.PublicUser_ViewLocationHistoryUI import PublicUser_LocationHistoryUI
from .boundary.PublicUser_ViewAffectedLocationUI import PublicUser_ViewAffectedLocationUI
from .boundary.PublicUser_ViewAlertUI import PublicUser_ViewAlertUI
from .boundary.PublicUser_AcknowledgeAlertUI import PublicUser_AcknowledgeAlertUI

# Boundary for Health Staff
from .boundary.HealthStaffUser_ViewPatientDetailsUI import HealthStaffUser_ViewPatientDetailsUI
from .boundary.HealthStaffUser_SendAlertPublicUI import HealthStaffUser_SendAlertPublicUI
from .boundary.HealthStaffUser_SendAlertBusinessUI import HealthStaffUser_SendAlertBusinessUI

# Boundary for Business Staff
from .boundary.BusinessUser_ViewAlertUI import BusinessUser_ViewAlertUI
from .boundary.BusinessUser_AcknowledgeAlertUI import BusinessUser_AcknowledgeAlertUI
from .boundary.BusinessUser_ViewAffectedOutletUI import BusinessUser_ViewAffectedOutletUI


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

		# If unsuccessful at updating
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
	publicUser_locationHistoryBoundary = PublicUser_LocationHistoryUI()

	return publicUser_locationHistoryBoundary.displayPage()

	# Get location history of current user
	locationHistory = public_locationHistoryController.getLocationHistory()
	
	return render_template('public_viewLocationHistory.html', userType=userLoginController.getUserType(),
															  locationHistory=locationHistory)

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

		# Set the boundary to contain the patient's NRIC
		healthStaffUser_viewPatientDetailsBoundary.setPatient(NRIC)

		# Get submit response 
		response = healthStaffUser_viewPatientDetailsBoundary.onSubmit()

		# Display Error if any
		if response != healthStaffUser_viewPatientDetailsBoundary.RESPONSE_SUCCESS:
			return healthStaffUser_viewPatientDetailsBoundary.displayError(response)

		# Display Success
		return healthStaffUser_viewPatientDetailsBoundary.displaySuccess()

@app.route('/view_update_vaccination', methods=['GET', 'POST'])
@loginRequired
def viewUpdateVaccination():
	if request.method == 'GET':
		return render_template('healthStaff_viewUpdateVaccination.html')
	if request.method == 'POST':
		return render_template('healthStaff_viewUpdateVaccination.html')
				
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
