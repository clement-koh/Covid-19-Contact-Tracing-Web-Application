from flask import render_template, request, redirect, send_from_directory, flash, jsonify
from .app import app
from .controllers.userLoginController import userLoginController
from .controllers.public_locationHistoryController import public_locationHistoryController
from .controllers.public_affectedLocationController import public_affectedLocationController
from .controllers.public_manageAlertController import public_manageAlertController
from .controllers.healthStaffUser_viewUserDetails import healthStaffUser_viewUserDetails
from .controllers.healthStaffUser_SendAlertController import healthStaffUser_SendAlertController
from .controllers.settingsController import settingsController
from .controllers.updatePersonalDetailsController import updatePersonalDetailsController


# -----------------------------------------------------
#                   Common Pages
# -----------------------------------------------------
@app.route('/', methods=['GET'])
@userLoginController.loginRequired
def overviewPage():
	return render_template('overview.html', userType = userLoginController.getUserType(),
											healthStatus = 'Green')

@app.route('/logout', methods=['GET'])
@userLoginController.loginRequired
def logout():
		userLoginController.logout()
		flash('Logged out successfully')
		return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
	# If user is using a getMethod
	if request.method == 'GET':
		# If user is already logged in
		if userLoginController.isAuthenticated():
			return redirect('/')
		# If not logged in, show login screen
		return render_template('login.html')

	if request.method == 'POST':
		# Get form details
		NRIC = request.form['username']
		password = request.form['password']

		# Attempt to log in
		loginAttempt = userLoginController.login(NRIC, password)
		
		# If login is successful, send to main page
		if loginAttempt[0]:
			return redirect('/')

		# If login is unsuccessful
		return render_template('login.html', errorMessage=loginAttempt[1])


@app.route('/view_alert', methods=['GET', 'POST'])
@userLoginController.loginRequired
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


# -----------------------------------------------------
#                   Public User Pages
# -----------------------------------------------------
@app.route('/view_location_history', methods=['GET'])
@userLoginController.loginRequired
def viewLocationHistoryPage():
	# Get location history of current user
	locationHistory = public_locationHistoryController.getLocationHistory()
	
	return render_template('public_viewLocationHistory.html', userType=userLoginController.getUserType(),
															  locationHistory=locationHistory)

@app.route('/view_affected_location', methods=['GET'])
@userLoginController.loginRequired
def viewAffectedLocationPage():
	return render_template('public_viewAffectedLocations.html', userType=userLoginController.getUserType())

#------------------------------------------------------
#update Particulars 
@app.route('/updateParticulars', methods=['GET', 'POST'])
@userLoginController.loginRequired
def updateParticularsPage():

    #get firstName 
    firstname = updatePersonalDetailsController.getFirstName()

    #get lastname
    lastname = updatePersonalDetailsController.getLastName()

    #get mobile
    mobile = updatePersonalDetailsController.getMobile()
    
    if request.method == 'POST':

        # Get form details
        mobile = request.form['mobile']

        result = updatePersonalDetailsController.updateRecord(mobile)


         # If successful
        if result[0]:
            flash(result[1], 'message')
        
        else:
            flash(result[1], 'error')

    return render_template('updateParticulars.html', firstname=firstname, lastname=lastname ,mobile=mobile)

#------------------------------------------------------
#setting
@app.route('/settings', methods=['GET', 'POST'])
@userLoginController.loginRequired
def settingsPage():
    
    if request.method == 'POST':

        # Get form details
        currentpassword = request.form["currentpassword"]
        password = request.form['password']
        confirmpassword = request.form["confirmpassword"]


        
        #check if password equal to confirm password
        if password != confirmpassword:
            flash('Password not Match', 'error')
            
        #check password at least 5 character 
        elif len(password) < 5:
            flash('Password at least 5 characters', 'error')

        #allow to change password
        else:
            result = settingsController.updatePassword(currentpassword,password)


            # If successful
            if result[0]:
                flash(result[1], 'message')
            
            else:
                flash(result[1], 'error')

    return render_template('settings.html')


# -----------------------------------------------------
#                   Health Staff Pages
# -----------------------------------------------------
@app.route('/send_alert', methods=['GET', 'POST'])
@userLoginController.loginRequired
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
def viewPatientDetailsPage():
	# Check if user has permission for this function
	currentUserType = userLoginController.getUserType()
	if currentUserType != 'Health Staff':
		flash('You do not have permission to access the requested functionality','error')
		return redirect('/')
	
	userDetails = healthStaffUser_viewUserDetails.getUserSearchDetails()
	if request.method == 'POST':
		# Get form details
		NRIC = request.form['user']
		
		# Get Search Fields details
		patientDetails = healthStaffUser_viewUserDetails.getUserDetails(NRIC)

		# If valid user input
		if patientDetails is not None:
			return render_template('healthStaff_viewUserDetails.html', userType=currentUserType,
																	   userDetails=userDetails,
																	   patientDetails=patientDetails)
		
		# If invalid user input
		flash("'{}' is not a valid user".format(NRIC), 'error')

	return render_template('healthStaff_viewUserDetails.html', userType=currentUserType,
															   userDetails=userDetails)

# @app.route('/test', methods=['GET'])
# @userLoginController.loginRequired
# def testpage():
#     return 'test successful'

# ---------------------------------------------------------
# 						 AJAX CALL
# --------------------------------------------------------
@app.route('/view_location_history/get_history', methods=['POST'])
def getAffectedLocationData():
	days_ago = int(request.form['days_ago'])
	if days_ago >= 0:
		return jsonify(public_affectedLocationController.getInfectedLocationHistory2(days_ago))

