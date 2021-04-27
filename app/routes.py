from flask import render_template, request, send_from_directory, flash, jsonify, session
from ..run import app, loginRequired

# Boundary for Users
from .boundary.User_LoginUI import User_LoginUI
from .boundary.User_LogoutUI import User_LogoutUI
from .boundary.User_UpdateContactUI import User_UpdateContactUI
from .boundary.User_ChangePasswordUI import User_ChangePasswordUI

# Boundary for Public Users
from .boundary.PublicUser_ViewLocationHistoryUI import PublicUser_LocationHistoryUI
from .boundary.PublicUser_ViewAffectedLocationUI import PublicUser_ViewAffectedLocationUI

# Boundary for Health Staff
from .boundary.HealthStaffUser_ViewPatientDetailsUI import HealthStaffUser_ViewPatientDetailsUI

from .controllers.public_affectedLocationController import public_affectedLocationController
from .controllers.public_manageAlertController import public_manageAlertController
from .controllers.healthStaffUser_viewUserDetails import healthStaffUser_viewUserDetails
from .controllers.healthStaffUser_SendAlertController import healthStaffUser_SendAlertController



# -----------------------------------------------------
#                   Common Pages
# -----------------------------------------------------
@app.route('/', methods=['GET'])
@loginRequired
def overviewPage():
	return render_template('overview.html', userType = session['userType'],
											healthStatus = 'Red')

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
		username = request.form['username']
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
	currentUserType = userLoginController.getUserType()
	if currentUserType not in ['Public', 'Business']:
		flash('You do not have permission to access the requested functionality', 'error')
		return redirect('/')

	# Update mark as read first
	if request.method == 'POST':
		id = request.form['alert_id']
		result = public_manageAlertController.markAsRead(id)

		if result[0]:
			flash(result[1], 'message')
		else:
			flash(result[1], 'error')

	# Get all alerts
	all_alerts = public_manageAlertController.getAllAlerts()

	return render_template('public_viewAlert.html', userType=userLoginController.getUserType(),
													all_alerts=all_alerts)


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
@app.route('/send_alert', methods=['GET', 'POST'])
@loginRequired
def sendAlertPage():
	# Check if user has permission for this function
	currentUserType = userLoginController.getUserType()
	if currentUserType != 'Health Staff':
		flash('You do not have permission to access the requested functionality','error')
		return redirect('/')
	
	# Get Search Fields details
	userDetails = healthStaffUser_SendAlertController.getUserSearchDetails()
	businessDetails = healthStaffUser_SendAlertController.getBusinessSearchDetails()

	if request.method == 'POST':
		# Get form details
		category = request.form['category']
		recipient = request.form['target']
		message = request.form['message']

		result = healthStaffUser_SendAlertController.newAlert(category, recipient, message)
		
		# If successful
		if result[0]:
			flash(result[1], 'message')
		else:
			flash(result[1], 'error')

	return render_template('healthStaff_new_alert.html', userType=currentUserType,
														 userDetails=userDetails,
														 businessDetails=businessDetails)

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
		NRIC = request.form['user']

		# Set the boundary to contain the patient's NRIC
		healthStaffUser_viewPatientDetailsBoundary.setPatient(NRIC)

		# Get submit response 
		response = healthStaffUser_viewPatientDetailsBoundary.onSubmit()

		# Display Error if any
		if response != healthStaffUser_viewPatientDetailsBoundary.RESPONSE_SUCCESS:
			return healthStaffUser_viewPatientDetailsBoundary.displayError(response)

		# Display Success
		return healthStaffUser_viewPatientDetailsBoundary.displaySuccess()
		

	# # Check if user has permission for this function
	# currentUserType = userLoginController.getUserType()
	# if currentUserType != 'Health Staff':
	# 	flash('You do not have permission to access the requested functionality','error')
	# 	return redirect('/')
	
	# userDetails = healthStaffUser_viewUserDetails.getUserSearchDetails()
	# if request.method == 'POST':
	# 	# Get form details
	# 	NRIC = request.form['user']
		
	# 	# Get Search Fields details
	# 	patientDetails = healthStaffUser_viewUserDetails.getUserDetails(NRIC)

	# 	# If valid user input
	# 	if patientDetails is not None:
	# 		return render_template('healthStaff_viewUserDetails.html', userType=currentUserType,
	# 																   userDetails=userDetails,
	# 																   patientDetails=patientDetails)
		
	# 	# If invalid user input
	# 	flash("'{}' is not a valid user".format(NRIC), 'error')

	# return render_template('healthStaff_viewUserDetails.html', userType=currentUserType,
	# 														   userDetails=userDetails)

# @app.route('/test', methods=['GET'])
# @userLoginController.loginRequired
# def testpage():
#     return 'test successful'
