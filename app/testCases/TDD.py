from ..boundary.User_LoginUI import User_LoginUI
from flask import Flask, render_template, session, redirect
import os

import unittest

class LoginTestCases(unittest.TestCase):
	def setUp(self):
		# Create boundary object
		self.boundary = User_LoginUI()

		# Set up application settings
		template_dir = os.path.abspath('./app/templates')
		static_dir = os.path.abspath('./app/static')
		self.app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
		self.app.secret_key="mykey123456"
		
		# Set display of result differences to unlimited
		self.maxDiff = None

	def test_displayPage(self):
		with self.app.test_request_context() as c:
			result = self.boundary.displayPage()
			expectedResult = render_template('login.html')
			errorMessage = 'Failed to display the login page'
			self.assertEqual(result, expectedResult, errorMessage)
	
	def test_onSubmit_publicUser_acceptCorrectValues(self):
		with self.app.test_request_context() as c:
			result = self.boundary.onSubmit('S0001', 'S0001')
			expectedResult = 'Success'
			errorMessage = 'onSubmit() with correct values did not return Success'
			self.assertEqual(result, expectedResult, errorMessage)

	def test_onSubmit_rejectWrongCredentials(self):
		result = self.boundary.onSubmit('S0001', '1111')
		expectedResult = 'Username or Password is incorrect'
		errorMessage = 'onSubmit() with incorrect values returned Success'
		self.assertEqual(result, expectedResult, errorMessage)

	def test_onSubmit_rejectSuspendedAccount(self):
		with self.app.test_request_context() as c:
			result = self.boundary.onSubmit('S0777', 'S0777')
			expectedResult = 'Account is suspended'
			errorMessage = 'onSubmit() with suspended account credentials returned Success'
			self.assertEqual(result, expectedResult, errorMessage)

	def test_isLoginFieldsEmpty_acceptNonEmptyFields(self):
		result = self.boundary.isLoginFieldsEmpty('S0001', 'S0001')
		expectedResult = False
		errorMessage = 'isLoginFieldsEmpty() with non-empty fields did not return False'
		self.assertEqual(result, expectedResult, errorMessage)

	def test_isLoginFieldsEmpty_rejectEmptyFields(self):
		result = self.boundary.isLoginFieldsEmpty('', '')
		expectedResult = True
		errorMessage = 'isLoginFieldsEmpty() with empty fields did not return True'
		self.assertEqual(result, expectedResult, errorMessage)
	
	def test_checkUserLoggedIn_acceptUnauthenticatedUser(self):
		with self.app.test_request_context() as c:
			result = self.boundary.checkUserLoggedIn()
			expectedResult = False
			errorMessage = 'checkUserLoggedIn() with unauthenticated user did not return False'
			self.assertEqual(result, expectedResult, errorMessage)
	
	def test_checkUserLoggedIn_rejectAuthenticatedUser(self):
		with self.app.test_request_context() as c:
			session['isAuthenticated'] = True
			result = self.boundary.checkUserLoggedIn()
			expectedResult = True
			errorMessage = 'checkUserLoggedIn() with authenticated user did not return True'
			self.assertEqual(result, expectedResult, errorMessage)
	
	def test_displaySuccess_displaySuccessPage(self):
		result = self.boundary.displaySuccess().location
		expectedResult = redirect('/').location
		errorMessage = 'Failed to redirect to overview page'
		self.assertEqual(result, expectedResult, errorMessage)
	
	def test_displayError_displayErrorPage(self):
		with self.app.test_request_context() as c:
			session['userType'] = 'Public'
			result = self.boundary.displayError("error")
			expectedResult = render_template('login.html', errorMessage="error")
			errorMessage = 'Failed to display the expected page'
			self.assertEqual(result, expectedResult, errorMessage)

if __name__ == "__main__":
	unittest.main()