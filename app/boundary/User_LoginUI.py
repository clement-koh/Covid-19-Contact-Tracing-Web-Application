from flask import render_template, redirect, session
from ..controllers.User_LoginController import User_LoginController 

class User_LoginUI:
	# Constructor
	def __init__(self):
		# Define responses status for the class
		self.RESPONSE_SUCCESS = "Success"
		self.RESPONSE_INVALID_CREDENTIALS = "Username or Password is incorrect"
		self.RESPONSE_ACCOUNT_SUSPENDED = "Account is suspended"

	# Public Method
	def displayPage(self):
		"""Displays the login page"""
		return render_template('login.html')

	def onSubmit(self, NRIC, password):
		"""
		Firstly, verify the user's NRIC and password, then check if account 
		is suspended. Return a response based on the outcome of each check.
		"""
		# initialise a User_LoginController
		controller = User_LoginController()

		# If credentials is incorrect
		if not controller.validateLogin(NRIC, password):
			return self.RESPONSE_INVALID_CREDENTIALS

		# If account is suspended
		if not controller.validateAccountStatus(NRIC):
			return self.RESPONSE_ACCOUNT_SUSPENDED
		
		# Otherwise, account is valid and active
		# Provide a session and return a success status
		session['isAuthenticated'] = True
		session['user'] = NRIC
		session['userType'] = controller.getAccountType(NRIC)
		session['viewingNRIC'] = None

		return self.RESPONSE_SUCCESS

	def isLoginFieldsEmpty(self, NRIC, password):
		""" 
		Returns True if the NRIC and password fields are empty
		"""
		# Checks if NRIC and password is empty
		if NRIC and password:
			return False
		return True

	def checkUserLoggedIn(self):
		"""
		Returns True if there is a user already logged in
		If a session does not exist, create a session and 
		set isAuthenticated to false
		"""
		try:
			return session['isAuthenticated']
		except:
			session['isAuthenticated'] = False
			return session['isAuthenticated']

	def displaySuccess(self):
		"""
		Redirects the user to the main page of the application
		"""
		return redirect('/')		

	def displayError(self, message):
		"""
		Display the login page, with an error message
		"""
		return render_template('login.html', errorMessage=message)