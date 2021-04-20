from flask import render_template, request, redirect, send_from_directory, flash
from .app import app
from .controllers.userLoginController import userLoginController
from .controllers.healthStaffUser_SendAlertController import healthStaffUser_SendAlertController
from .controllers.receiveAlertController import receiveAlertController


# -----------------------------------------------------
#                   Common Pages
# -----------------------------------------------------
@app.route('/', methods=['GET'])
@userLoginController.loginRequired
def index():
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

@app.route("/alerts", methods=['GET', 'POST'])
@userLoginController.loginRequired
def alerts():
    currentUserType = userLoginController.getUserType()
    if currentUserType not in ['Public', 'Business']:
        flash('You do not have permission to access the requested functionality', 'error')
        return redirect('/')

    all_alerts = receiveAlertController.getAllAlerts()

    if request.method == 'POST':
        id = request.form['alert_id']
        print(id)
        result = receiveAlertController.markAsRead(id)

        if result[0]:
            flash(result[1], 'message')
        flash(result[1], 'error')
    
    return render_template('alert.html', all_alerts=all_alerts)


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

    # Set color of flash
    flashColor = None

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

@app.route('/contact_tracing', methods=['GET', 'POST'])
@userLoginController.loginRequired
def contactTracingPage():
    # Check if user has permission for this function
    currentUserType = userLoginController.getUserType()
    if currentUserType != 'Health Staff':
        flash('You do not have permission to access the requested functionality','error')
        return redirect('/')
    
    # Get Search Fields details
    userDetails = healthStaffUser_SendAlertController.getUserSearchDetails()
    businessDetails = healthStaffUser_SendAlertController.getBusinessSearchDetails()

    # Set color of flash
    flashColor = None

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

    return render_template('healthStaff_contact_tracing.html', userType=currentUserType,
                                                               userDetails=userDetails,
                                                               businessDetails=businessDetails)

# @app.route('/business_search', methods=['POST'])
# @userLoginController.loginRequired
# def searchBusiness():
#     # Check if user has permission for this function
#     if userLoginController.getUserType() != 'Health Staff':
#         flash("You do not have permission to access this functionality")
#         return redirect('/')

#     return render_template('healthStaff_new_alert.html', searchDetails='')



@app.route('/test', methods=['GET'])
@userLoginController.loginRequired
def testpage():
    return 'test successful'