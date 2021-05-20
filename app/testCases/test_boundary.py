from ..boundary.HealthStaffUser_SendAlertPublicUI import HealthStaffUser_SendAlertPublicUI
from flask import Flask, session, render_template, redirect
import os

import unittest

class testCases_HealthStaffUser_SendAlertPublic(unittest.TestCase):
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
		with self.app.test_request_context() as c:
			session['userType'] = 'Health Staff'
			result = self.boundary.displayPage()
			self.assertEqual(result, render_template('healthStaff_new_public_alert.html', userType="Health Staff"), "Failed to display the expected webpage")
	
	def test_displayPage_preventsAccessForPublicUser(self):
		with self.app.test_request_context() as c:
			session['userType'] = 'Public'
			result = self.boundary.displayPage()
			self.assertNotEqual(result, render_template('healthStaff_new_public_alert.html', userType="Public"), "Public User has unauthorized access to webpage")

	def test_displayPage_preventsAccessForBusinessUser(self):
		with self.app.test_request_context() as c:
			session['userType'] = 'Business'
			result = self.boundary.displayPage()
			self.assertNotEqual(result, render_template('healthStaff_new_public_alert.html', userType="Business"), "Business User has unauthorized access to webpage")

	def test_displayPage_preventsAccessForOrganisationUser(self):
		with self.app.test_request_context() as c:
			session['userType'] = 'Organisation'
			result = self.boundary.displayPage()
			self.assertNotEqual(result, render_template('healthStaff_new_public_alert.html', userType="Organisation"), "Organisation User has unauthorized access to webpage")

	def test_onSubmit_acceptCorrectValues(self):
		with self.app.test_request_context() as c:
			session['user'] = 'S1999'
			result = self.boundary.onSubmit("S0999", "Message from BOUNDARY test case with correct values")
			self.assertEqual(result, "Alert successfully sent to 'S0999'", "onSubmit with correct values did not return Success")
	
	def test_onSubmit_rejectIncorrectNRIC(self):
		result = self.boundary.onSubmit("S9999", "Message from test case with incorrect NRIC")
		self.assertEqual(result, "Recipient('S9999') is not a valid user", "onSubmit with incorrect NRIC did not return the correct error")

	def test_onSubmit_rejectEmptyNRIC(self):
		result = self.boundary.onSubmit("", "Message with empty NRIC")
		self.assertEqual(result, "Fields cannot be empty", "onSubmit with blank NRIC did not return the correct error")

	def test_onSubmit_rejectEmptyMessage(self):
		result = self.boundary.onSubmit("S0999", "")
		self.assertEqual(result, "Fields cannot be empty", "onSubmit with blank message did not return the correct error")

	def test_displayError_displayErrorPage(self):
		with self.app.test_request_context() as c:
			session['userType'] = 'Health Staff'
			result = self.boundary.displayError("error")
			self.assertEqual(result, render_template('healthStaff_new_public_alert.html', userType="Health Staff"), "Failed to display the expected webpage")

	def test_displaySuccess_displaySuccessPage(self):
		with self.app.test_request_context() as c:
			session['userType'] = 'Health Staff'
			result = self.boundary.displaySuccess()
			self.assertEqual(result, render_template('healthStaff_new_public_alert.html', userType="Health Staff"), "Failed to display the expected webpage")

if __name__ == '__main__':
	unittest.main(verbosity=2)