from ..boundary.HealthStaffUser_SendAlertPublicUI import HealthStaffUser_SendAlertPublicUI
from flask import Flask, session, render_template, redirect
import os

import unittest

class testCases_HealthStaffUser_SendAlertPublicUI(unittest.TestCase):
	def setUp(self):
		# Create boundary object
		self.boundary = HealthStaffUser_SendAlertPublicUI()

		# Setup Application Settings
		template_dir = os.path.abspath('./app/templates')
		static_dir = os.path.abspath('./app/static')
		self.app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
		self.app.secret_key="mykey123456"
		
		# Set display of result differences to unlimited
		self.maxDiff = None

	def test_displayPage_allowsAccessForHealthStaffUser(self):
		# Setting Session Context
		with self.app.test_request_context() as c:
			session['userType'] = 'Health Staff'

			result = self.boundary.displayPage()
			expectedResult = render_template('healthStaff_new_public_alert.html', userType="Health Staff")
			errorMsg = "Failed to display the expected webpage"
			self.assertEqual(result, expectedResult, errorMsg)
	
	def test_displayPage_preventsAccessForPublicUser(self):
		# Setting Session Context
		with self.app.test_request_context() as c:
			session['userType'] = 'Public'

			result = self.boundary.displayPage()
			expectedResult = render_template('healthStaff_new_public_alert.html', userType="Public")
			errorMsg = "Public User has unauthorized access to webpage"
			self.assertNotEqual(result, expectedResult, errorMsg)

	def test_displayPage_preventsAccessForBusinessUser(self):
		# Setting Session Context
		with self.app.test_request_context() as c:
			session['userType'] = 'Business'

			result = self.boundary.displayPage()
			expectedResult = render_template('healthStaff_new_public_alert.html', userType="Business")
			errorMsg = "Business User has unauthorized access to webpage"
			self.assertNotEqual(result, expectedResult, errorMsg)

	def test_displayPage_preventsAccessForOrganisationUser(self):
		# Setting Session Context
		with self.app.test_request_context() as c:
			session['userType'] = 'Organisation'

			result = self.boundary.displayPage()
			expectedResult = render_template('healthStaff_new_public_alert.html', userType="Organisation")
			errorMsg = "Organisation User has unauthorized access to webpage"
			self.assertNotEqual(result, expectedResult, errorMsg)

	def test_onSubmit_acceptCorrectValues(self):
		# Setting Session Context
		with self.app.test_request_context() as c:
			session['user'] = 'S1999'

			result = self.boundary.onSubmit("S0999", "Message from BOUNDARY test case with correct values")
			expectedResult = "Alert successfully sent to 'S0999'"
			errorMsg = "onSubmit with correct values did not return Success"
			self.assertEqual(result, expectedResult, errorMsg)
	
	def test_onSubmit_rejectIncorrectNRIC(self):
		with self.app.test_request_context() as c:
			session['user'] = 'S1999'

			result = self.boundary.onSubmit("S9999", "Message from test case with incorrect NRIC")
			expectedResult = "Recipient('S9999') is not a valid user"
			errorMsg = "onSubmit with incorrect NRIC did not return the correct error"
			self.assertEqual(result, expectedResult, errorMsg)

	def test_onSubmit_rejectEmptyNRIC(self):
		with self.app.test_request_context() as c:
			session['user'] = 'S1999'

			result = self.boundary.onSubmit("", "Message with empty NRIC")
			expectedResult = "Fields cannot be empty"
			errorMsg = "onSubmit with blank NRIC did not return the correct error"
			self.assertEqual(result, expectedResult, errorMsg)

	def test_onSubmit_rejectEmptyMessage(self):
		with self.app.test_request_context() as c:
			session['user'] = 'S1999'
			
			result = self.boundary.onSubmit("S0999", "")
			expectedResult = "Fields cannot be empty"
			errorMsg = "onSubmit with blank message did not return the correct error"
			self.assertEqual(result, expectedResult, errorMsg)

	def test_displayError_displayErrorPage(self):
		# Setting Session Context
		with self.app.test_request_context() as c:
			session['userType'] = 'Health Staff'

			result = self.boundary.displayError("error")
			expectedResult = render_template('healthStaff_new_public_alert.html', userType="Health Staff")
			errorMsg = "Failed to display the expected webpage"
			self.assertEqual(result, expectedResult, errorMsg)

	def test_displaySuccess_displaySuccessPage(self):
		# Setting Session Context
		with self.app.test_request_context() as c:
			session['userType'] = 'Health Staff'

			result = self.boundary.displaySuccess()
			expectedResult = render_template('healthStaff_new_public_alert.html', userType="Health Staff")
			errorMsg = "Failed to display the expected webpage"
			self.assertEqual(result, expectedResult, errorMsg)

if __name__ == '__main__':
	unittest.main(verbosity=2)